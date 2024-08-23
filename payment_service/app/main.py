from fastapi import FastAPI, HTTPException
from app.kafka.consumers.order_response_consumer import consume_order_messages
from app.kafka.producers.payment_producer import produce_payment_message

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start consuming messages from the order topic
    await consume_order_messages()

@app.post("/process_payment/")
async def process_payment(order_id: int, product_name: str):
    # Mock payment processing logic
    payment_success = True  # For testing, assume payment is successful

    if payment_success:
        # Produce a message to the payment topic
        await produce_payment_message(order_id, product_name, "paid")
        return {"status": "Payment processed", "order_id": order_id}
    else:
        raise HTTPException(status_code=400, detail="Payment failed")
