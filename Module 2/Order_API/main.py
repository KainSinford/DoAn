from flask import Flask, request, jsonify
from db import insert_order
from rabbitmq import publish_order

app = Flask(__name__)

@app.route("/api/orders", methods=["POST"])
def create_order():
    data = request.json

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    # Validate
    if not user_id or not product_id or quantity <= 0:
        return jsonify({"error": "Invalid data"}), 400

    # Insert MySQL (PENDING)
    order_id = insert_order(user_id, product_id, quantity)

    # Publish RabbitMQ
    publish_order({
        "order_id": order_id,
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity
    })

    return jsonify({
        "message": "Order received",
        "order_id": order_id
    }), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)