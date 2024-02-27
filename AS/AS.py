import socket
import json

try:
    with open("dns_records.json", "r") as file:
        dns_records = json.load(file)
except FileNotFoundError:
    dns_records = []

AS_IP = "0.0.0.0"
AS_PORT = 53533

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((AS_IP, AS_PORT))

print("Authoritative Server (AS) is running on port 53533...")

while True:
    data, address = udp_socket.recvfrom(1024)

    message = data.decode().strip().splitlines()
    # print(message)
    if len(message) == 4 and message[0] == "TYPE=A":
        type, name, value, ttl = message  

        type = type.split("=")[1]
        name = name.split("=")[1]
        value = value.split("=")[1]
        ttl = int(ttl.split("=")[1])

        existing_record = next((record for record in dns_records if record["NAME"] == name), None)

        if existing_record:
            existing_record["TYPE"] = type
            existing_record["VALUE"] = value
            existing_record["TTL"] = ttl
            print(f"Updated Record: {existing_record}")
        else:
            record = {
                "TYPE": type,
                "NAME": name,
                "VALUE": value,
                "TTL": ttl
            }
            dns_records.append(record)
            print(f"Registered: {record}")

        with open("dns_records.json", "w") as file:
            json.dump(dns_records, file, indent=4)  

        response = "Registration successful".encode()
        udp_socket.sendto(response, address)
    elif len(message) == 2 and message[0] == "TYPE=A":
        _, query_name = message
        matching_records = [record for record in dns_records if record["NAME"] == query_name.split("=")[1]]
        print(matching_records)
        if matching_records:
            response_record = matching_records[0]
            response = f"TYPE={response_record['TYPE']}\nNAME={response_record['NAME']}\nVALUE={response_record['VALUE']}\nTTL={response_record['TTL']}".encode()
            status_code=200
        else:
            response = "Record not found".encode()
            status_code=200
        udp_socket.sendto(response, address)
    else:
        error_response = "Invalid request".encode()
        udp_socket.sendto(error_response, address)
