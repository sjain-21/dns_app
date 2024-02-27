from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)


@app.route('/fibonacci', methods=['GET'])
def calculate_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if hostname is None or fs_port is None or number is None or as_ip is None or as_port is None:
        return jsonify(error="Bad Request: Missing Parameters"), 400

    try:
        fs_port = int(fs_port)
        number = int(number)
        as_port = int(as_port)
    except ValueError:
        return jsonify(error="Bad Request: Invalid Port or Number"), 400

    dns_query = f"TYPE=A\nNAME={hostname}"
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(dns_query.encode(), (as_ip, as_port))
    response, address = udp_socket.recvfrom(1024)
    print(response.decode())
    if response.decode() == "Record not found":
        response_code = 404  
        message = "DNS Record not found"
        fibonacci_result = None
    else:
        udp_socket.close()
        response_lines = response.decode().split('\n')
        _, _, fs_ip, _ = response_lines[0], response_lines[1], response_lines[2], response_lines[3]
        fs_ip = fs_ip.split("=")[1]
        fs_server_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        fs_response = requests.get(fs_server_url)

        # print(fs_response)
        # print(fs_response.status_code)
        # print(fs_response.json())
        message=""
        if fs_response.status_code == 200:
            fs_data = fs_response.json()
            fibonacci_result = fs_data.get('fibonacci')
            response_code = 200
            message="success"
        else:
            fs_data = fs_response.json()
            response_code = fs_response.status_code
            fibonacci_result = None
            message=fs_data.get('error')
    

    response_data = {
        "response_code": response_code,
        "fibonacci_result": fibonacci_result,
        "response_message": message
    }

    return jsonify(response_data), 200

app.run(host='0.0.0.0',
        port=8080,
        debug=True)
