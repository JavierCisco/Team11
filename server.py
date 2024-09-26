import socket

server_address = ('localhost', 7501)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(server_address)

print(f"Server is listening on {server_address[0]}:{server_address[1]}")

while True:
	data, client_address = server_socket.recvfrom(1024)
	print(f"Received message: {data.decode()} from{client_address}")
	response = "Equipment code received"
	server_socket.sendto(response.encode(), client_address)

