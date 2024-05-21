import os
import sys
import json
import pika

def consumer(
    host: str,
    port: str,
    queue_name: str,
    routing_key: str,
    exchange: str,
):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
            )
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange=exchange,
            exchange_type="direct",
        )

        channel.queue_declare(
            queue=queue_name,
            # exclusive=True,
        )

        # queue_name = result.method.queue

        channel.queue_bind(
            queue=queue_name,
            exchange=exchange,
            routing_key=routing_key,
        )

        def callback(ch, method, properties, body):
            payload = json.loads(body)
            print(" [x] Received ")
            print(payload)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == "__main__":
    consumer(
        host="rabbit_mq",
        port="5672",
        queue_name="email",
        routing_key="email",
        exchange="email",
    )
