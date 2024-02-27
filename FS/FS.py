from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

registration_info = {}

def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

@app.route('/register', methods=['PUT'])
def register_server():
    try:
        data = request.get_json()
        hostname = data.get('hostname')
        ip = data.get('ip')
        as_ip = data.get('as_ip')
        as_port = data.get('as_port')

        if hostname and ip:
            # Format hostname and IP according to the specified format
            # formatted_hostname = "\n".join([f"NAME={segment}" for segment in hostname.split('.')])
            formatted_hostname = f"NAME={hostname}"
            formatted_ip = f"VALUE={ip}"
            
            # DNS message in the specified format
            dns_message = f"TYPE=A\n{formatted_hostname}\n{formatted_ip}\nTTL=10"

            # UDP server address and port for Authoritative Server (AS)
            AS_IP = as_ip
            AS_PORT = int(as_port)
            
            # Create a UDP socket and send registration request to AS
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.sendto(dns_message.encode(), (AS_IP, AS_PORT))
            response, address = udp_socket.recvfrom(1024)
            print(response.decode())
            udp_socket.close()

            # Store registration information
            registration_info['hostname'] = hostname
            registration_info['ip'] = ip

            return jsonify(message="Registration successful"), 201
        else:
            return jsonify(error="Bad Request: Missing Parameters"), 400
    except Exception as e:
        return jsonify(error="Internal Server Error"), 500

@app.route('/fibonacci', methods=['GET'])
def calculate_fibonacci():
    try:
        number = int(request.args.get('number'))
        if number < 0:
            raise ValueError
        result = fibonacci(number)
        return jsonify(fibonacci=result), 200
    except (ValueError, TypeError):
        return jsonify(error="Bad Request: Invalid Number Format"), 400

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
