from flask import Flask, request, jsonify
from db import insert_order
from rabbitmq import publish_order
from models import Order

app = Flask(__name__)

@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.json

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    # Tạo object từ model
    order = Order.from_dict(data)

    # Validate an toàn
    if not order.user_id or not order.product_id or not order.quantity or order.quantity <= 0:
        return jsonify({"error": "Invalid data"}), 400

    try:
        # Insert MySQL (PENDING)
        order_id = insert_order(
            order.user_id,
            order.product_id,
            order.quantity
        )

        order.order_id = order_id

        # Publish RabbitMQ
        publish_order(order.to_dict())

        return jsonify({
            "message": "Order received",
            "order_id": order_id
        }), 202

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
