import socket
import json
import time
import os
import logging as log_handler

log_handler.basicConfig(format='[%(asctime)s %(filename)s:%(lineno)d] %(message)s',
                        datefmt='%H:%M:%S',
                        level=log_handler.DEBUG)

SERVER_ADDR = "0.0.0.0"
BIND_PORT = 53533
DATA_CHUNK = 1024
DB_PATH = "/tmp/dns_records.json"

def init_server_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SERVER_ADDR, BIND_PORT))
    return s

def load_dns_records():
    if not os.path.isfile(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({}, f, indent=4)
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_dns_records(records):
    with open(DB_PATH, "w") as f:
        json.dump(records, f, indent=4)

def handle_received_data(data):
    if len(data) == 4:
        domain, address, r_type, duration = data
        records = load_dns_records()
        expiration = time.time() + int(duration)
        records[domain] = {"address": address, "type": r_type, "expiration": expiration}
        save_dns_records(records)
        return None
    elif len(data) == 2:
        query_type, queried_domain = data
        records = load_dns_records()
        if queried_domain not in records:
            return None
        else:
            record = records[queried_domain]
            if time.time() > record["expiration"]:
                return None
            return (record["type"], queried_domain, record["address"], record["expiration"] - time.time())
    else:
        return f"Unexpected data length: {len(data)}"

def run_server():
    server_socket = init_server_socket()
    log_handler.info(f"Server active on {SERVER_ADDR}:{BIND_PORT}")

    while True:
        byte_data, client_endpoint = server_socket.recvfrom(DATA_CHUNK)
        data = json.loads(byte_data)
        log_handler.debug(f"Received: {data}")
        result = handle_received_data(data)
        if result:
            response = json.dumps(result).encode()
        else:
            response = b""
        server_socket.sendto(response, client_endpoint)

if __name__ == '__main__':
    log_handler.debug("Initializing server...")
    run_server()
