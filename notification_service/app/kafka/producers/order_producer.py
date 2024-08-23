# from aiokafka import AIOKafkaProducer
# from app.settings import KAFKA_BROKER_URL, KAFKA_ORDER_TOPIC
# import json
# import asyncio

# async def produce_order_placed_message(product_id: int, quantity: int):
#     producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)
#     await producer.start()
#     try:
#         message = {
#             "product_id": product_id,
#             "quantity": quantity
#         }
#         await producer.send_and_wait(KAFKA_ORDER_TOPIC, json.dumps(message).encode('utf-8'))
#         print(f"Message sent to Kafka: {message}")
#     except Exception as e:
#         print(f"Failed to send message to Kafka: {str(e)}")
#     finally:
#         await producer.stop()
