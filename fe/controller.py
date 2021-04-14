#!flask/bin/python
from flask import Flask, request, Response
import json
#import producer as prod
import pika
import uuid


connection = None
callback_queue = None
channel = None

routes=None
users=None
corr_id = None
response = None



app = Flask(__name__)

@app.route ('/v1/routes/<route_id>', methods=['GET'])
def get_route(route_id):
    #routeid = route_id
    if not route_id:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
    
    data = json.dumps({ "data": {"routes_id":str(route_id)}, "operation": "r"})
    routes = send_get(data,'r')
    
    if (routes):
        return Response(routes, status=200, mimetype='application/json')
    return Response("{'message':'Routes not found'}", status=200, mimetype='application/json')

@app.route ('/v1/routes', methods=['GET'])
def get_routes():
    
    username = request.args.get('username')
    date = request.args.get('date')
    city = request.args.get('city')
    
    #if (not username or username is None) or (not date or date is None) or (not city or city is None):
    if not username or not date or not city:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
    
    data = json.dumps({ "data": { "routes_id": "", "username": username, "date": date, "city": city }, "operation": "r"})
    routes = send_get(data,'r')
    
    if (routes):
        return Response(routes, status=200, mimetype='application/json')
    return Response("{'message':'Routes not found'}", status=200, mimetype='application/json')
    
@app.route ('/v1/routes', methods=['POST'])
def add_routes(): 
    print(request)
    json_data = request.json
    print(json_data)
    rid = json_data['routes_id']
    username = json_data['username']
    date = json_data['date']
    city = json_data['city']
    route = json_data['route']
    if not username or not date or not city or not route or not rid:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
    
    data = json.dumps({ "data": json_data, "operation": "c"})
    send(data,'r')
    return Response("{'message':'OK'}", status=201, mimetype='application/json')
    
@app.route ('/v1/routes', methods=['PUT'])
def update_routes():
    json_data = request.json
    rid = json_data['routes_id']
    username = json_data['username']
    date = json_data['date']
    city = json_data['city']
    route = json_data['route']
    if not username or not date or not city or not route or not rid:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
    
    data = json.dumps({ "data": json_data, "operation": "u"})
    send(data,'r')
    return Response("{'message':'OK'}", status=202, mimetype='application/json')
    
@app.route ('/v1/routes/<route_id>', methods=['DELETE'])
def delete_routes(): 
    routeid = route_id
    if not routeid:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
        
    data = json.dumps({ "data": {"routes_id":str(routeid)}, "operation": "d"})
    print
    send(data,'r')
    return Response("{'message':'OK'}", status=202, mimetype='application/json')
    
@app.route ('/v1/users/<user_id>', methods=['GET'])
def get_users(user_id):
    username = user_id
    if not username:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
    
    data = json.dumps({ "data": {"username":str(username) }, "operation": "r"})
    users = send_get(data,'u')
    
    if (users):
        return Response(users, status=200, mimetype='application/json')
    return Response("{'message':'Routes not found'}", status=200, mimetype='application/json')
    
@app.route ('/v1/users', methods=['POST'])
def add_users(): 
    json_data = request.json
    username = json_data['username']
    password = json_data['password']
    email = json_data['email']
    country = json_data['country']
    if not username or not password or not email or not country:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
    
    data = json.dumps({ "data": json_data, "operation": "c"})
    send(data,'u')
    return Response("{'message':'OK'}", status=201, mimetype='application/json')
    
@app.route ('/v1/users', methods=['PUT'])
def update_users():
    json_data = request.json
    username = json_data['username']
    password = json_data['password']
    email = json_data['email']
    country = json_data['country']
    if not username or not password or not email or not country:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
    
    data = json.dumps({ "data": json_data, "operation": "u"})
    send(data,'u')
    return Response("{'message':'OK'}", status=202, mimetype='application/json')
    
@app.route ('/v1/users/<user_id>', methods=['DELETE'])
def delete_users(): 
    username = user_id
    if not username:
        return Response("{'message':'Bad Request Error'}", status=400, mimetype='application/json')
        
    data = json.dumps({ "data": {"username":str(username)}, "operation": "d"})
    send(data,'u')
    return Response("{'message':'OK'}", status=202, mimetype='application/json')

def send(data_input, type_call):
    print(" [x] Sending %r" % data_input)
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))
    channel = connection.channel()

    # Create a new direct exchange
    if type_call == 'r':
    	exch = 'exchange_routes'
    elif type_call == 'u':
        exch = 'exchange_users'
    channel.exchange_declare(exchange=exch, exchange_type ='direct')
    # Create a queue (not mandatory)
    #channel.queue_declare(queue='routes')

    # Send the message
    # No need to specify routing key because we have exchange
    channel.basic_publish(exchange=exch, routing_key='routes', body=str(data_input))
    
    # Close the channel
    connection.close()
    
def send_get(data_input, type_call):
    print(" [x] Sending %r" % data_input)
    #connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))
    #channel = connection.channel()
    
    #channel_resp = connection.channel()
    #result = channel_resp.queue_declare(queue='',exclusive=True)
    #callback_queue = result.method.queue
    global corr_id
    corr_id = str(uuid.uuid4())
    print(corr_id)

    # Create a new direct exchange
    if type_call == 'r':
    	exch = 'exchange_routes'
    	rout_key = 'routes'
    elif type_call == 'u':
        exch = 'exchange_users'
        rout_key = 'users'
    print(rout_key)
    channel.exchange_declare(exchange=exch, exchange_type ='direct')	
    # Create a queue (not mandatory)
    #channel.queue_declare(queue='routes')
    # Send the message
    channel.basic_publish(exchange=exch, 
    	routing_key=rout_key, 
    	body=str(data_input),
    	properties=pika.BasicProperties(
    		reply_to=callback_queue,
    		correlation_id=corr_id))
    print(" [x] Waiting for response")
    while response is None:
    	connection.process_data_events(time_limit=10)
    #connection.close()
    print(response)
    return response

def on_response(ch, method, properties, body):
    print(" [X] Received %r" % body)
    print(properties.correlation_id)
    print(corr_id)
    if corr_id == properties.correlation_id:
        print(corr_id)
        global response
        response = body

if __name__ == '__main__':
    
    print("started")
    #channel_resp = connection.channel()
    #result = channel_resp.queue_declare(queue='',exclusive=True)
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))
    channel = connection.channel()
    result = channel.queue_declare(queue='',exclusive=True)
    callback_queue = result.method.queue
    channel.basic_consume(
	queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True)
        
    app.run(host='0.0.0.0', port=8080)
