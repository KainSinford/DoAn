import time
import json
from rabbitmq import consume_orders
from db_mysql import update_order_status
from db_postgres import insert_transaction

def process_order(ch, method, properties, body):
    data = json.loads(body)

    order_id = data["order_id"]

    print(f"Processing order {order_id}")

    # Giả lập xử lý
    time.sleep(2)

    # Insert PostgreSQL
    insert_transaction(data)

    # Update MySQL
    update_order_status(order_id, "COMPLETED")

    # ACK
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    consume_orders(process_order)

if __name__ == "__main__":
    main()