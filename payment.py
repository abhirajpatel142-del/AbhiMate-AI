import os
import razorpay

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)

def create_order(amount=9900):
    data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    }

    return client.order.create(data=data)
