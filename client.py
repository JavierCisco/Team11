import socket
import threading

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

print(msg)

def process_traffic(message):
    global red_team, green_team, action_log

    try:
        attacker_id, target_id = message.split(":")
    except ValueError:
        print(f"Invalid message: {message}")
        return

    # Find the attacker and target in teams
    for team in [red_team, green_team]:
        for i, player in enumerate(team):
            if player[0] == attacker_id:
                team[i] = (player[0], player[1] + 100)  # Update score
                action_log.append(f"{player[0]} hit {target_id}")
                if len(action_log) > 5:
                    action_log.pop(0)
                print(f"{player[0]} hit {target_id}, score updated!")

def udp_listener():
    print("Client is handling traffic...")
    while True:
        message, address = UDPClientSocket.recvfrom(bufferSize)
        message = message.decode('utf-8')
        print(f"Received traffic: {message}")
        process_traffic(message)

# Start the listener in a separate thread
listener_thread = threading.Thread(target=udp_listener, daemon=True)
listener_thread.start()
