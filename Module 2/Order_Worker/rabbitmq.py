import pika

def consume_orders(callback):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )
    channel = connection.channel()

    channel.queue_declare(queue='order_queue', durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue='order_queue',
        on_message_callback=callback
    )

    print("Waiting for messages...")
    channel.start_consuming()
