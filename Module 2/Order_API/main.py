from flask import Flask, request, jsonify
from db import insert_order
from rabbitmq import publish_order
from models import Order
import logging
import os

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.json

    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    order = Order.from_dict(data)

    if (
        order.user_id is None or
        order.product_id is None or
        order.quantity is None or
        order.quantity <= 0
    ):
        return jsonify({"error": "Invalid data"}), 400

    try:
        order_id = insert_order(
            order.user_id,
            order.product_id,
            order.quantity
        )

        order.order_id = order_id

        publish_order(order.to_dict())

        logger.info(f"Order created: {order_id}")

        return jsonify({"order_id": order_id}), 202

    except Exception as e:
        logger.error(e)
        return jsonify({"error": "Internal error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
