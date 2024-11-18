import socket

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 7501)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
def send_test_signal(signal):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 7500
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(signal.encode('utf-8'), (UDP_IP, UDP_PORT))
    print(f"Sent signal: {signal}")

send_test_signal("202")
print(msg)
