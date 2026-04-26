class Order:
    def __init__(self, user_id, product_id, quantity, status="PENDING", order_id=None):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.status = status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Order(
            user_id=data.get("user_id"),
            product_id=data.get("product_id"),
            quantity=data.get("quantity"),
            status=data.get("status", "PENDING"),
            order_id=data.get("order_id")
        )
