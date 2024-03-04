from flask import Flask, request
import socket
import requests
import pickle

server_instance = Flask(__name__)
DATA_SIZE = 2048

@server_instance.route('/')
def server_intro():
    return 'Welcome to the User Server (US)'

def fetch_server_ip(host, auth_server_ip, auth_server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(pickle.dumps(("A", host)), (auth_server_ip, auth_server_port))
        data, _ = s.recvfrom(DATA_SIZE)
    _, _, fetched_ip, _ = pickle.loads(data)
    return fetched_ip

@server_instance.route('/fibonacci', methods=['GET'])
def compute_fibonacci():
    host_name = request.args.get('hostname').strip('"')
    fib_server_port = int(request.args.get('fs_port'))
    sequence_num = int(request.args.get('number'))
    auth_server_ip = request.args.get('as_ip').strip('"')
    auth_server_port = int(request.args.get('as_port'))

    server_ip = fetch_server_ip(host_name, auth_server_ip, auth_server_port)
    if not server_ip:
        return "Error fetching server IP"

    fib_response = requests.get(f"http://{server_ip}:{fib_server_port}/fibonacci", params={"number": sequence_num})
    return fib_response.content

if __name__ == '__main__':
    server_instance.run(host='0.0.0.0', port=8080, debug=True)
