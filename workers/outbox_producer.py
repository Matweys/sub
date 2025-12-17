# workers/outbox_producer.py
import asyncio
import json
import os
from datetime import datetime, timezone, timedelta

from aiokafka import AIOKafkaProducer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.db import engine
from products.outbox_model import OutboxEvent

# ====== НАСТРОЙКИ ======
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9094")  # на хосте у тебя 9094
BATCH_SIZE = int(os.getenv("OUTBOX_BATCH_SIZE", "50"))
POLL_INTERVAL = float(os.getenv("OUTBOX_POLL_INTERVAL", "0.5"))
WORKER_ID = os.getenv("OUTBOX_WORKER_ID", f"worker-{os.getpid()}")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


def utcnow():
    return datetime.now(timezone.utc)


async def fetch_and_lock_batch(session):
    """
    Берём пачку pending событий и лочим их на этот воркер.
    FOR UPDATE SKIP LOCKED защищает от конкуренции нескольких воркеров.
    """
    stmt = (
        select(OutboxEvent)
        .where(
            OutboxEvent.status == "pending",
            OutboxEvent.available_at <= utcnow(),
        )
        .order_by(OutboxEvent.created_at.asc())
        .with_for_update(skip_locked=True)
        .limit(BATCH_SIZE)
    )

    res = await session.execute(stmt)
    events = list(res.scalars().all())

    for e in events:
        e.locked_at = utcnow()
        e.locked_by = WORKER_ID

    return events


async def mark_sent(event_id):
    async with SessionLocal() as session:
        async with session.begin():
            obj = await session.get(OutboxEvent, event_id, with_for_update=True)
            obj.status = "sent"
            obj.sent_at = utcnow()
            obj.locked_at = None
            obj.locked_by = None
            obj.last_error = None


async def mark_failed(event_id, err: Exception):
    async with SessionLocal() as session:
        async with session.begin():
            obj = await session.get(OutboxEvent, event_id, with_for_update=True)
            obj.attempts += 1
            obj.last_error = str(err)
            obj.locked_at = None
            obj.locked_by = None

            # backoff: 5s * attempts, максимум 60s
            delay = min(60, 5 * obj.attempts)
            obj.available_at = utcnow() + timedelta(seconds=delay)


async def run():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
    await producer.start()
    try:
        while True:
            async with SessionLocal() as session:
                async with session.begin():
                    events = await fetch_and_lock_batch(session)

            if not events:
                await asyncio.sleep(POLL_INTERVAL)
                continue

            for e in events:
                try:
                    value = json.dumps(e.payload).encode("utf-8")
                    key = (e.key or e.aggregate_id).encode("utf-8")
                    await producer.send_and_wait(e.topic, value=value, key=key)

                    await mark_sent(e.id)

                except Exception as ex:
                    await mark_failed(e.id, ex)

            await asyncio.sleep(0)  # yield
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(run())
