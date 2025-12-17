# workers/product_events_consumer.py
import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9094")
TOPIC = os.getenv("PRODUCT_EVENTS_TOPIC", "product-events")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "product-events-consumer")


async def main():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id=GROUP_ID,
        enable_auto_commit=False,      # "по-взрослому": коммитим offset сами
        auto_offset_reset="earliest",  # если группа новая — читать с начала
    )

    await consumer.start()
    try:
        print(f"[consumer] started. topic={TOPIC}, group_id={GROUP_ID}, bootstrap={KAFKA_BOOTSTRAP}")
        async for msg in consumer:
            try:
                payload = json.loads(msg.value.decode("utf-8"))
                # минимальная “бизнес-реакция”
                if payload.get("event") == "ProductCreated":
                    p = payload.get("product", {})
                    print(f"✅ Product created: id={p.get('id')} name={p.get('name')} owner={p.get('owner')}")
                else:
                    print(f"ℹ️ event received: {payload}")

                # коммитим offset только после успешной обработки
                await consumer.commit()

            except Exception as ex:
                # если ошибка — offset не коммитим, сообщение будет перечитано
                print(f"❌ error processing message: {ex}. raw={msg.value!r}")

    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
