import pika
import json
import time
import os

def get_connection():
    while True:
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST"))
            )
        except:
            print("RabbitMQ chưa sẵn sàng...")
            time.sleep(3)


def publish_order(order_data):
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue='order_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=json.dumps(order_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
