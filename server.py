import socket

localIP     = "127.0.0.1"
localPort   = 7501
bufferSize  = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address and ip
# UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

def send_test_signal(signal):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 7500
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(signal.encode('utf-8'), (UDP_IP, UDP_PORT))
    print(f"Sent signal: {signal}")

send_test_signal("202")

# Listen for incoming datagrams
try:
    while(True):
    
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        
        # print(clientMsg)
        # print(clientIP)
    
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, address)
finally:
    UDPServerSocket.close()
