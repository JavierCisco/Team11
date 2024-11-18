import socket

localIP     = "127.0.0.1"
localPort   = 7500
bufferSize  = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

def send_start_signal(address):
    message = b"202"
    UDPServerSocket.sendto(message, address)
    print("Start signal sent to traffic generator")

def send_stop_signal(address):
    message = b"221"
    UDPServerSocket.sendto(message, address)
    print("Stop signal sent to traffic generator")

# Listen for incoming datagrams
try:
    while(True):
    
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        
        print(clientMsg)
        print(clientIP)
    
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)
finally:
    UDPServerSocket.close()
