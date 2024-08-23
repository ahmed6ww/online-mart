

from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
KAFKA_BROKER_URL = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_INVENTORY_TOPIC = config("KAFKA_INVENTORY_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PRODUCT", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY = config("KAFKA_CONSUMER_GROUP_ID_FOR_INVENTORY", cast=str)

KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
