import subprocess
import socket



# Functions to start the server and client
def start_server():
    subprocess.Popen(['python3', 'server.py'])  # Start the UDP server

def start_client():
    subprocess.Popen(['python3', 'client.py'])  # Start the UDP client

# UDP setup
UDP_IP = "127.0.0.1"  # replace with your target IP
UDP_PORT = 7500       # the port to broadcast equipment codes
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_equipment_code(code):
    message = str(code).encode('utf-8')
    udp_socket.sendto(message, (UDP_IP, UDP_PORT))
    print(f"Sent equipment code: {code}")