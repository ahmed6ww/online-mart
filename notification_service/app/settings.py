from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
KAFKA_BROKER_URL = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_ORDER = config("KAFKA_CONSUMER_GROUP_ID_FOR_ORDER", cast=str)

EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USERNAME = config("EMAIL_USERNAME", cast=str)
EMAIL_PASSWORD = config("EMAIL_PASSWORD", cast=str)
EMAIL_FROM = config("EMAIL_FROM", cast=str)

