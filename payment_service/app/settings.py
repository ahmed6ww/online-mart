from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()



DATABASE_URL = config("DATABASE_URL", cast=str)
KAFKA_BROKER_URL = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_ORDER_TOPIC = config("KAFKA_ORDER_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT = config("KAFKA_CONSUMER_GROUP_ID_FOR_PAYMENT", cast=str)
KAFKA_PAYMENT_TOPIC = config("KAFKA_PAYMENT_TOPIC", cast=str)
