import pika
import json
import threading

import traceback
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='stock_topic', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange with a routing pattern
channel.queue_bind(exchange='stock_topic', queue=queue_name, routing_key='#')

def callback(ch, method, properties, body):
    
    import traceback
    
    print("----------------------application traceback---------------------",method)
    traceback.print_stack()
    routing_key = method.routing_key
    message = json.loads(body)
    print(f"Received {routing_key} message: {message}")
    print("\n\napplication", threading.current_thread().getName())
    print("\n\napplicationthreadid",threading.get_ident())

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

