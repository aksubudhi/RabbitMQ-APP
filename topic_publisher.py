import pika
from flask import Flask, render_template, request, json
app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=5000))
channel = connection.channel()
channel.exchange_declare(exchange='stock_topic', exchange_type='topic')

stocks = ['Stock A', 'Stock B', 'Stock C']

@app.route('/')
def index():
    return render_template('sender.html', stocks=stocks, message=None)

@app.route('/send_stock', methods=['POST'])
def send_stock():
    selected_stock = request.form['stock']
    price = request.form['price']

    send_dict = {selected_stock: price}
    send_json = json.dumps(send_dict)

    # Use the selected_stock as the routing key
    channel.basic_publish(exchange='stock_topic', routing_key=selected_stock, body=send_json)
    message = f"Sent {selected_stock} price {price}"
    return render_template('sender.html', stocks=stocks, message=message)

if __name__ == '__main__':
    app.run(port=8009)

