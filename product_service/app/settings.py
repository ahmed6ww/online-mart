

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

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)
