import socket
import threading
import time
from asyncio import sleep

# Constants for ports, format, and server address
RECEIVE_PORT = 7501
BROADCAST_PORT = 7500
FORMAT = 'utf-8'
SERVER = '127.0.0.1'
RECEIVE_ADDR = (SERVER, RECEIVE_PORT)
BROADCAST_ADDR = (SERVER, BROADCAST_PORT)

class Server:

    global play1_hit
    global play2_hit

    def __init__(self):
        print('[DEBUG] Initializing server...')
        try:
            # Initialize sockets for receiving and broadcasting
            self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.server_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_recv.bind(RECEIVE_ADDR)
            
            self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            self.server_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_thread = threading.Thread(target=self.start)
            self.server_thread.start()

            self.last_update = 0
            self.up_arr = []
            self.action_log = None
            
            self.player_points = {}
            self.team_points = {"TeamGreen": 0, "TeamRed": 0}

            print('[DEBUG] Server initialized successfully.')
        except Exception as e:
            print(f'[ERROR] Error during server initialization: {e}')
            raise

    def start(self):
        print(f'[LISTENING] Server is listening on {RECEIVE_PORT}')

        # Main loop to listen for incoming messages
        while True:
            data, addr = self.server_recv.recvfrom(1024)
            if data:
                print(f'[RECEIVED] Data from {addr}: {data.decode(FORMAT)}')
                client_thread = threading.Thread(target=self.handle_client, args=(data.decode(FORMAT),))
                client_thread.start()

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
        self.server_recv.close()
        self.server_broadcast.close()

    def handle_client(self, msg: str):
        print(f'[DEBUG] Received message: {msg}')

        transmit_id, hit_id = None, None  # Default values

        if ':' in msg:
            parts = msg.split(':')
            if len(parts) == 2:
                transmit_id, hit_id = parts
                print(f'{transmit_id}:{hit_id}')
                self.send_hit_id(transmit_id, hit_id)
            else:
                print(f'[ERROR] Malformed message. Expected "player_id:hit_id", got: {msg}')
        elif msg.isdigit():
            print(f'[SINGLE ID RECEIVED] Message: {msg}')
            # Handle single ID messages if needed
            self.server_broadcast.sendto(msg.encode(FORMAT), BROADCAST_ADDR)
        else:
            print(f'[ERROR] Unrecognized message format: {msg}')

        # if transmit_id and hit_id:
        #     play1_hit = transmit_id
        #     play2_hit = hit_id
        #     if self.action_log:
        #         if hit_id == 43:  # Green Base hit
        #             if transmit_id % 2 == 0:
        #                 print(f'[GREEN BASE HIT] Friendly fire by {transmit_id}')
        #             else:
        #                 points = 100
        #                 message = f'Player {transmit_id} hit Green Base!'
        #                 # if self.action_log:
        #                 self.action_log.add_line(message,color=(0, 255, 0))
        #         elif hit_id == 53:  # Red Base hit
        #             if transmit_id % 2 != 0:
        #                 print(f'[RED BASE HIT] Friendly fire by {transmit_id}')
        #             else:
        #                 points = 100
        #                 message = f'Player {transmit_id} hit Red Base!'
        #                 # if self.action_log:
        #                 self.action_log.add_line(message,color=(0, 255, 0))
        #     else:
        #         self.action_log.add_line(f'Player {transmit_id} hit Player {hit_id}')
            # print('[DEBUG] transmit_id or hit_id was set.')
            # print(f'{play1_hit} & {play2_hit}')

        # else:
        #     print('[DEBUG] transmit_id or hit_id was not set.')
   
        

    # def send_to_actionlog(self, equip_id: str, hit_id: str):
        # Log to TextScroll if available
        # if self.action_log:

        #     if hit_id == 43:  # Green Base hit
        #         if equip_id % 2 == 0:
        #             print(f'[GREEN BASE HIT] Friendly fire by {equip_id}')
        #         else:
        #             points = 100
        #             message = f'Player {equip_id} hit Green Base!'
        #             if self.action_log:
        #                 self.action_log.add_line(message,color=(0, 255, 0))
        #     elif hit_id == 53:  # Red Base hit
        #         if equip_id % 2 != 0:
        #             print(f'[RED BASE HIT] Friendly fire by {equip_id}')
        #         else:
        #             points = 100
        #             message = f'Player {equip_id} hit Red Base!'
        #             if self.action_log:
        #                 self.action_log.add_line(message,color=(0, 255, 0))
        #     else:
        #         message = f'Player {equip_id} hit Player {hit_id}'
        #         self.action_log.add_line(message,color=(0, 255, 0))
                
        # print(f'[DEBUG] Action Log Message: {equip_id} hit {hit_id}')

    def send_hit_id(self, equip_id_str: str, hit_id_str: str):
        equip_id = int(equip_id_str)
        hit_id = int(hit_id_str)
        points = 0
        message = ''
        print(f"equip_id: {equip_id}, hit_id: {hit_id}")

        if self.action_log:
            if hit_id == 43:  # Green Base hit
                if equip_id % 2 == 0:
                    print(f'[GREEN BASE HIT] Friendly fire by {equip_id}')
                    message = f'Friendly fire by Player {equip_id} hit Green Base!'
                    #self.action_log.add_line(message)
                else:
                    points = 100
                    message = f'Player {equip_id} hit Green Base!'
                    #if self.action_log:
                    #self.action_log.add_line(message)
            elif hit_id == 53:  # Red Base hit
                if equip_id % 2 != 0:
                    print(f'[RED BASE HIT] Friendly fire by {equip_id}')
                    message = f'Friendly fire by Player {equip_id} hit Red Base!'
                    #self.action_log.add_line(message)
                else:
                    points = 100
                    message = f'Player {equip_id} hit Red Base!'
                    #if self.action_log:
                    #self.action_log.add_line(message)
            elif (equip_id + hit_id) % 2 == 0:  # Friendly fire between players
                points = -10
                message = f'Player {equip_id} hit friendly {hit_id}'
            else:  # Valid hit
                points = 10
                message = f'Player {equip_id} hit Player {hit_id}'

        self.update_points(equip_id, hit_id, points)

        if message:
            print(f'[BROADCASTING] Sending message: {message}')
            self.action_log.add_line(message)
            self.server_broadcast.sendto(message.encode(FORMAT), BROADCAST_ADDR)

    def update_points(self, equip_id: int, hit_id: int, points: int):
        
        if equip_id not in self.player_points:
            self.player_points[equip_id] = 0
        self.player_points[equip_id] += points

        # Update team points
        if equip_id % 2 == 0:
            team = "TeamGreen"
        else:
            team = "TeamRed"

        self.team_points[team] += points
        print(f'[PLAYER POINTS] {self.player_points}')
        print(f'[TEAM POINTS] {self.team_points}')
        # print(f'[POINTS UPDATE] Equip ID: {equip_id}, Hit ID: {hit_id}, Points: {points}')

    def get_scores(self):
        # Returns both player and team scores
        return {
            "player_points": self.player_points,
            "team_scores": self.team_scores,
        }
