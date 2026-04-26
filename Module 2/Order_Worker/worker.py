import json
import pika
import time
import os
import logging

from db_postgres import insert_transaction
from db_mysql import update_order_status

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def get_connection():
    while True:
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"))
            )
        except Exception as e:
            logger.warning(f"RabbitMQ connection failed: {e}. Retrying in 3 seconds...")
            time.sleep(3)


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)

        insert_transaction(data)
        update_order_status(data["order_id"], "COMPLETED")

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"Processed order {data['order_id']}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        
        headers = properties.headers or {}
        retry_count = headers.get("x-retry", 0)

        if retry_count >= 3:
            logger.error(f"Drop message after 3 retries: {data}")
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge to remove from queue
        else:
            logger.warning(f"Retry {retry_count + 1}/3")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def consume():
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue='order_queue', durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue='order_queue',
        on_message_callback=callback
    )

    print("Worker started...")
    channel.start_consuming()


if __name__ == "__main__":
    consume()
