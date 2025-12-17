# products/exceptions.py
class ProductError(Exception):
    """Базовая ошибка домена products."""


class PermissionDenied(ProductError):
    """Нет прав на действие."""


class ProductCreateError(ProductError):
    """Не удалось создать продукт (ошибка БД/валидации/и т.п.)."""


class ProductGetAllError(ProductError):
    """Не удалось получить все продукты (ошибка БД/валидации/и т.п.)."""


class ProductGetOwnerError(ProductError):
    """Не удалось получить продукт для пользователя (ошибка БД/валидации/и т.п.)."""
