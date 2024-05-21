"""Producer of messages that the other workers will process.
"""
import json
import pika


def rabbit_mq_sender(
    message_data: dict,
    host: str,
    port: int,
    queue_name: str,
    routing_key: str,
    exchange: str,
):
    """
    Function for direct connection with the RabbitMQ tail.

    Parameters
    ----------
    message: Dict[str, Any]
        Message to send.
    host:str
        IP of the connection of Rabbit in string form.
    port: str
        Port number (add it as a string) of the host we are connecting to.
    queue_name: str
        Name of the queue.
    routing_key: str
        Name of the route
    exchange: str
        Name of the exchange
    """
    message = json.dumps(message_data)

    # creating the sending signal of the object/message to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
        )
    )
    channel = connection.channel()
    channel.queue_declare(
        queue=queue_name
    )
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            content_type='text/plain'
        )
    )
    connection.close()
