import socket
import pickle
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
DB_PATH = "/tmp/data_store.json"
DATA_TYPE = "A"

def init_server_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SERVER_ADDR, BIND_PORT))
    return s

def handle_received_data(data):
    if len(data) == 4:
        domain, address, r_type, duration = data
        if not os.path.isfile(DB_PATH):
            with open(DB_PATH, "w") as f:
                json.dump({}, f, indent=4)
        with open(DB_PATH, "r") as f:
            current_records = json.load(f)
        expiration = time.time() + int(duration)
        current_records[domain] = (address, expiration, duration)
        with open(DB_PATH, "w") as f:
            json.dump(current_records, f, indent=4)
        return None
    elif len(data) == 2:
        query_type, queried_domain = data
        with open(DB_PATH, "r") as f:
            current_records = json.load(f)
        if queried_domain not in current_records:
            return None
        else:
            address, expiration, duration = current_records[queried_domain]
            if time.time() > expiration:
                return None
            return (DATA_TYPE, queried_domain, address, expiration, duration)
    else:
        return f"Unexpected data length: {len(data)}"

def run():
    server_socket = init_server_socket()
    log_handler.info(f"Server active on "
                     f"{socket.gethostbyname(socket.gethostname())}:{BIND_PORT}")

    while True:
        byte_data, client_endpoint = server_socket.recvfrom(DATA_CHUNK)
        data = pickle.loads(byte_data)
        log_handler.debug(f"Received: {data}")
        result = handle_received_data(data)
        if result:
            _, domain, address, _, duration = result
            response = (DATA_TYPE, domain, address, duration)
        else:
            response = ""
        response_bytes = pickle.dumps(response)
        server_socket.sendto(response_bytes, client_endpoint)

if __name__ == '__main__':
    log_handler.debug("Initializing server...")
    run()
