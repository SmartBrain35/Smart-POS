# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ================= General App Settings =================
APP_NAME = "Smart POS"
DEBUG = os.getenv("DEBUG", "True") == "True"
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")

# ================= Database Configuration =================
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")  # Options: sqlite, postgresql, mysql
DB_NAME = os.getenv("DB_NAME", "smart_pos.db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "")

if DB_ENGINE.lower() == "sqlite":
    DATABASE_URL = f"sqlite:///{DB_NAME}"
elif DB_ENGINE.lower() == "postgresql":
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DB_ENGINE.lower() == "mysql":
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    raise ValueError("Unsupported DB_ENGINE. Use sqlite, postgresql, or mysql.")

# ================= Default Stock Settings =================
DEFAULT_MIN_QUANTITY_ALERT = int(os.getenv("DEFAULT_MIN_QUANTITY_ALERT", 5))
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "general")

# ================= Other Constants =================
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ================= Helper Functions =================
def get_database_url():
    """Return the configured database URL."""
    return DATABASE_URL
