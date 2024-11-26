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
scores = {"Red": {}, "Green": {}}
class Server():
    def __init__(self):
        # Initialize sockets for receiving and broadcasting
        self.server_recv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_recv.bind(BROADCAST_ADDR)

        # Initialize the server broadcasting socket
        self.server_broadcast = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Set the running flag to True for clean shutdown
        self.running = True

        # Start the server thread
        self.server_thread = threading.Thread(target=self.start)
        self.server_thread.start()

    
    def start(self):
        print(f'[LISTENING] Server is listening on {BROADCAST_PORT}')
        while self.running:
            try:
                data, addr = self.server_broadcast.recvfrom(1024)
                if data and self.running:
                    print(f'[RECEIVED] Data from {addr}: {data.decode(FORMAT)}')
                    threading.Thread(target=self.handle_client, args=(data.decode(FORMAT), addr)).start()
            except OSError as e:
                 if self.running:
                     print(f'[ERROR] Server encountered an error: {e}')
                     break

    def start_traffic(self):
        # Start the game by broadcasting code 202
        print('[BROADCASTING] Starting game with code 202')
        self.server_broadcast.sendto("202".encode(FORMAT), BROADCAST_ADDR)
    def stop(self):
        self.running = False  # Stop the server gracefully
        print('[BROADCASTING] Stopping game with code 221')
        for _ in range(3):
            try:
                self.server_broadcast.sendto("221".encode(FORMAT), BROADCAST_ADDR)
            except OSError:
                pass
            time.sleep(0.1)
        try:
            self.server_recv.close()
            self.server_broadcast.close()
        except OSError as e:
            print(f"[ERROR] Failed to close sockets: {e}")

    def handle_client(self, msg: str):
        try:
            if not self.running:
                return
            print(f'[DEBUG] Received message: {msg}')
            if ':' in msg:
                attacker, target = msg.split(":")
                self.update_points(attacker, target)
                log_entry = f"{attacker} hit {target}"
                action_log.append(log_entry)
                print(f'[LOG] {log_entry}')  # Log the hit
                self.send_hit_id(attacker, target)
                #parts = msg.split(':')
            elif msg.isdigit():
                print(f'[SINGLE ID RECEIVED] Message: {msg}')
                self.server_broadcast.sendto(msg.encode(FORMAT), BROADCAST_ADDR)
            else:
                print(f'[ERROR] Unrecognized message format: {msg}')
        except OSError as e:
            if self.running:
                print(f'[ERROR] Error in handle_client: {e}')
            

        

    #def update_points(self, equip_id: int, hit_id: int, points: int):
    def update_points(self, attacker_id: str, target_id: str):
        for team, team_scores in scores.items():
            if attacker_id in team_scores:
                team_scores[attacker_id] += 10
                action_log.append(f"{attacker_id} hit {target_id}")
                print(f"[POINTS UPDATE] {attacker_id} scored! New Score: {team_scores[attacker_id]}")
                break
#         else:
#             print(f"[WARNING] Attacker {attacker_id} not found in any team.")
        # Placeholder for updating points in the game
        #print(f'[POINTS UPDATE] Equip ID: {equip_id}, Hit ID: {hit_id}, Points: {points}')

    def send_hit_id(self, transmit_id, hit_id):
        log_entry = f"{attacker} hit {target}"
        self.server_broadcast.sendto(log_entry.encode(FORMAT), BROADCAST_ADDR)
        print(f"[BROADCAST] {log_entry}")
#        log_entry = f"{transmit_id} hit {hit_id}"
#        print(f"[LOG] {log_entry}")
#        self.server_broadcast.sendto(log_entry.encode(FORMAT), BROADCAST_ADDR)

if __name__ == "__main__":
    try:
        server = Server()
        print("[INFO] Server is running. Press Ctrl+C to stop.")
        server.start_traffic()
        while server.running:  # Keep the main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down the server...")
        server.stop()  # Ensure the server stops gracefully
        print("[INFO] Server stopped")
