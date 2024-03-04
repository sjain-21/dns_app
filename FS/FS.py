from flask import Flask, request
import socket
import pickle

server = Flask(__name__)
DATA_SIZE = 1024

@server.route('/')
def welcome_message():
    return "Welcome to the Fibonacci Computation Server!"

def fibonacci_calculation(val):
    if val < 0:
        raise ValueError("Input should be non-negative")
    elif val == 0:
        return 0
    elif val in [1, 2]:
        return 1
    return fibonacci_calculation(val - 1) + fibonacci_calculation(val - 2)

@server.route('/fibonacci')
def compute_fibonacci():
    num = int(request.args.get('number'))
    return str(fibonacci_calculation(num))

def send_registration_data(payload, address):
    serialized_data = pickle.dumps(payload)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.sendto(serialized_data, address)

@server.route('/register', methods=['PUT'])
def register_server():
    details = request.json
    if not details:
        raise ValueError("No data provided in request")
    
    server_name = details["hostname"]
    fib_server_ip = details["fs_ip"]
    auth_server_ip = details["as_ip"]
    auth_server_port = details["as_port"]
    lifespan = details["ttl"]

    data_to_send = ((server_name, fib_server_ip, "A", lifespan))
    send_registration_data(data_to_send, (auth_server_ip, auth_server_port))
    
    return "Successfully Registered!"

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=9090, debug=True)
