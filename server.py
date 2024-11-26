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

# ACTION_LOG = ['testing', 'pls', 'work', 'i', 'beg', 'still', 'work']


class Server():
    def __init__(self):
        # Initialize sockets for receiving and broadcasting
        self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_recv.bind(BROADCAST_ADDR)
        self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_thread = threading.Thread(target=self.start)
        self.server_thread.start()

    def start(self):
        print(f'[LISTENING] Server is listening on {RECEIVE_PORT}')

        # Main loop to listen for incoming messages
        while True:
            # ACTION_LOG.append('update')
            data, addr = self.server_recv.recvfrom(1024)
            if data:
                print(f'[RECEIVED] Data from {addr}: {data.decode(FORMAT)}')
                client_thread = threading.Thread(target=self.handle_client, args=(data.decode(FORMAT),))
                client_thread.start()

    def start_traffic(self):
        # Start the game by broadcasting code 202
        print('[BROADCASTING] Starting game with code 202')
        ACTION_LOG.append('[BROADCASTING] Starting game with code 202')
        self.server_broadcast.sendto("202".encode(FORMAT), BROADCAST_ADDR)

    def stop(self):
        # Stop the game by broadcasting code 221 three times
        print('[BROADCASTING] Stopping game with code 221')
        for _ in range(3):
            self.server_broadcast.sendto("221".encode(FORMAT), BROADCAST_ADDR)
            time.sleep(0.1)
        self.server_recv.close()
        self.server_broadcast.close()

    def handle_client(self, msg: str):
        print(f'[DEBUG] Received message: {msg}')
        if ':' in msg:
            parts = msg.split(':')
            if len(parts) == 2:
                transmit_id, hit_id = parts
                print(f'[HIT EVENT] Transmit ID: {transmit_id}, Hit ID: {hit_id}')
                self.send_hit_id(transmit_id, hit_id)
            else:
                print(f'[ERROR] Malformed message. Expected "player_id:hit_id", got: {msg}')
        elif msg.isdigit():
            print(f'[SINGLE ID RECEIVED] Message: {msg}')
            # Handle single ID messages if needed
            self.server_broadcast.sendto(msg.encode(FORMAT), BROADCAST_ADDR)
        else:
            print(f'[ERROR] Unrecognized message format: {msg}')

    # def send_hit_id(self, equip_id_str: str, hit_id_str: str):
    #     # Handle hit events and update points accordingly
    #     equip_id = int(equip_id_str)
    #     hit_id = int(hit_id_str)
    #     points = 0
    #     message = ''

    #     if hit_id == 43:  # Green Base hit
    #         if equip_id % 2 == 0:
    #             print(f'[GREEN BASE HIT] Friendly fire by {equip_id}')
    #         else:
    #             points = 100
    #             message = f'{hit_id}'
    #     elif hit_id == 53:  # Red Base hit
    #         if equip_id % 2 != 0:
    #             print(f'[RED BASE HIT] Friendly fire by {equip_id}')
    #         else:
    #             points = 100
    #             message = f'{hit_id}'
    #     elif (equip_id + hit_id) % 2 == 0:  # Friendly fire between players
    #         points = -10
    #         message = f'{equip_id}'
    #     else:  # Valid hit
    #         points = 10
    #         message = f'{hit_id}'

    #     self.update_points(equip_id, hit_id, points)

    #     if message:
    #         print(f'[BROADCASTING] Sending message: {message}')
    #         self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)

    def update_points(self, equip_id: int, hit_id: int, points: int):
        # Placeholder for updating points in the game
        print(f'[POINTS UPDATE] Equip ID: {equip_id}, Hit ID: {hit_id}, Points: {points}')


if __name__ == "__main__":
    server = Server()
    # server.start_traffic()
