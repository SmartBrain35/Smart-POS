import os
from functools import lru_cache


class Settings:
    secret_key: str = os.getenv("SECRET_KEY")
    database_uri: str = os.getenv("DATABASE_URI", "sqlite:///app.db")
    config: str = os.getenv("CONFIG", "development")
    app_name: str = "Smart POS"
    debug: str = os.getenv("DEBUG", "True") == "True"
    default_currency: str = os.getenv("DEFAULT_CURRENCY", "USD")
    default_min_quantity_alert: int = int(os.getenv("DEFAULT_MIN_QUANTITY_ALERT", 5))
    default_category: str = os.getenv("DEFAULT_CATEGORY", "general")
    date_format: str = "%Y-%m-%d %H:%M:%S"


@lru_cache
def get_settings() -> Settings:
    return Settings()
