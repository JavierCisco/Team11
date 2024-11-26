import socket
import threading
import time

# Constants for ports, format, and server address
RECEIVE_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
RECEIVE_ADDR = (SERVER, RECEIVE_PORT)
BROADCAST_ADDR = (SERVER, BROADCAST_PORT)

class Server():
    def __init__(self):
        # Initialize sockets for receiving and broadcasting
        self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_recv.bind(BROADCAST_ADDR)
        self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_thread = threading.Thread(target=self.start)
        self.server_thread.start()

    def start(self):
        print(f'[LISTENING] Server is listening on {BROADCAST_PORT}')
        while True:
            try:
                data, addr = self.server_broadcast.recvfrom(1024)
                if data:
                    print(f'[RECEIVED] Data from {addr}: {data.decode(FORMAT)}')
                    threading.Thread(target=self.handle_client, args=(data.decode(FORMAT), addr)).start()
            except Exception as e:
                print(f'[ERROR] Server encountered an error: {e}')

    def start_traffic(self):
        # Start the game by broadcasting code 202
        print('[BROADCASTING] Starting game with code 202')
        self.server_broadcast.sendto("202".encode(FORMAT), BROADCAST_ADDR)

    def stop(self):
        # Stop the game by broadcasting code 221 three times
        print('[BROADCASTING] Stopping game with code 221')
        for _ in range(3):
            self.server_broadcast.sendto("221".encode(FORMAT), BROADCAST_ADDR)
            time.sleep(0.1)
        self.server_broadcast.close()
        print('[CLOSED] Broadcast socket successfully closed.')

    def handle_client(self, msg: str):
        if ":" in msg:
            transmitter, hit_id = map(int, msg.split(":"))
            team = "Red" if transmitter % 2 != 0 else "Green"
            if transmitter % 2 == hit_id % 2:  # Friendly fire
                points = -10
                broadcast_msg = str(transmitter)
            else:  # Opponent hit
                points = 10
                broadcast_msg = str(hit_id)
            self.update_points(transmitter, hit_id, points)
            self.server_broadcast.sendto(broadcast_msg.encode(FORMAT), BROADCAST_ADDR)
        elif msg == "43":  # Green Base Hit
            print("Message 43 received")
            self.update_points(None, None, 100)
        elif msg == "53":  # Red Base Hit
            print("Message 43 received")
            self.update_points(None, None, 100)
        else:
            print(f'[UNHANDLED MESSAGE] {msg}')

    def update_points(self, equip_id: int, hit_id: int, points: int):
        # Placeholder for updating points in the game
        print(f'[POINTS UPDATE] Equip ID: {equip_id}, Hit ID: {hit_id}, Points: {points}')


if __name__ == "__main__":
    server = Server()
