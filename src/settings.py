import os

APP_VERSION = os.environ.get('APP_VERSION', 'Unknown version')


# DB
DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
DB_PORT = os.getenv('DB_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'core-db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'develop')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'envelope')
DB_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# BACKEND
ALGORITHM = "HS256"
SECRET_KEY = os.getenv('SECRET_KEY', "bb861a8d76582fbf259eccb3fcda04069ee15966c9a7246336f0db67b446d78c")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60)
