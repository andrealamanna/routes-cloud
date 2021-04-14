import pika
import json
import mongo_interface as mongo

# Define a callback invoked every time a message is received
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print(properties.correlation_id)
    print(properties)
    payload = json.loads(body)
    operation = payload['operation']
    data = payload['data']
    if (operation == 'c'):
        mongo.create_routes(data)
    elif (operation == 'r'):
        routes = mongo.read_routes(data)
        if not routes:
            routes = "{'message': 'Not found'}"
        print(" [x] Sending %r" % routes)

        ch.basic_publish(exchange='',
        	routing_key=properties.reply_to,
                properties=pika.BasicProperties(correlation_id = properties.correlation_id),
                body=str(routes))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif (operation == 'u'):
        mongo.update_routes(data)
    elif (operation == 'd'):
        mongo.delete_routes(data)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.exchange_declare(exchange='exchange_routes', exchange_type ='direct')

# Let the system to create the queue name
result = channel.queue_declare (queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='exchange_routes',queue=queue_name, routing_key='routes')
# Subscribe to the queue and assign the callback with ack (in order to maintain the channel opened we don't use auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
