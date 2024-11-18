import pygame
import sys
import socket
import random
import subprocess
# additions -Ame
import threading
import time
# Only in between
from database import *

# initializing pygame
pygame.init()
pygame.mixer.init()

# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Splash Screen")

# load and display the splash image
try:
    splash_sound = pygame.mixer.Sound("theme.mp3")
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (800, 500))
except Exception as error:
    print("Error in Splash Screen: {error}")
    pygame.quit()
    sys.exit()
splash_sound.play()
# set a timer to show the main screen after 3 seconds
show_main_screen_event = pygame.USEREVENT + 1
pygame.time.set_timer(show_main_screen_event, 3000)

action_log = []

# Functions to start the server and client
def start_SC(file: str):
    subprocess.Popen(['python3', f'{file}.py'])  # Start the UDP server
# Call this functions to start the server and client
start_SC('server')
start_SC('client')

# UDP setup
# UDP_IP = "127.0.0.1"  # replace with your target IP
# UDP_PORT = 7500       # the port to broadcast equipment codes
# udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Constants for communication
SERVER = '127.0.0.1'
BROADCAST_PORT = 7500
RECEIVE_PORT = 7501
FORMAT = 'utf-8'

def send_equipment_code(code):
    message = str(code).encode(FORMAT)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.sendto(message, (SERVER, BROADCAST_PORT))
    print(f"Sent equipment code: {code}")

# Function to send messages to the server
def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.sendto(message.encode(FORMAT), (SERVER, BROADCAST_PORT))

# Function to receive messages from the server
def receive_message():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # udp_socket.bind(('127.0.0.1', RECEIVE_PORT))
        data, _ = udp_socket.recvfrom(1024)
        return data.decode(FORMAT)
    
# Handle game events received from the server
def process_game_event(message):
    global team_scores, action_log
    if message == "202":
        print("[GAME STARTED] Starting the game!")
        action_log.append("Game Started!")
    elif message == "221":
        print("[GAME ENDED] Stopping the game.")
        action_log.append("Game Ended!")
    elif ":" in message:
        transmit_id, hit_id = message.split(":")
        action_log.append(f"Player {transmit_id} hit Player {hit_id}")
        update_score("Red" if int(transmit_id) % 2 != 0 else "Green", 10)
    elif message == "43":
        action_log.append("Green Base Hit! +100 Points")
        update_score("Green", 100)
    elif message == "53":
        action_log.append("Red Base Hit! +100 Points")
        update_score("Red", 100)
    else:
        print(f"[UNKNOWN EVENT] Received: {message}")
        action_log.append(f"Unknown Event: {message}")

# Update scores for teams
team_scores = {"Red": 0, "Green": 0}

def update_score(team, points):
    if team in team_scores:
        team_scores[team] += points
        print(f"[SCORE UPDATE] {team} Team: {team_scores[team]} points")

# Thread to listen for updates from the server
def listen_for_updates():
    while True:
        message = receive_message()
        process_game_event(message)

# TextBox class for table cells
class TextBox:
    def __init__(self, x, y, width, height, table_id=None, row=None, col=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('black')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.font = pygame.font.Font(None, 20)
        self.active = False
        self.table_id = table_id
        self.row = row
        self.col = col

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
    
    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.active = True
            return self.table_id, self.row, self.col
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(100, text_surface.get_width() + 10)

# Create two tables of text boxes (2 columns x 10 rows each)
table1 = []
table2 = []
cell_width = 100
cell_height = 40
selected_row = None
selected_col = None
red_team = []
green_team = []

# Table 1 (left side - columns 1 and 2)
for row in range(10):
    table_row = []
    for col in range(2):
        x = 100 + col * cell_width
        y = 50 + row * cell_height
        table_row.append(TextBox(x, y, cell_width, cell_height, table_id=0, row=row, col=col))
    table1.append(table_row)

# Table 2 (right side - columns 3 and 4)
for row in range(10):
    table_row = []
    for col in range(2):
        x = 450 + col * cell_width
        y = 50 + row * cell_height
        table_row.append(TextBox(x, y, cell_width, cell_height, table_id=1, row=row, col=col))
    table2.append(table_row)

# Combine both tables
tables = [table1, table2]

# button class
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text_lines = text.split('\n')
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.font = pygame.font.Font(None, 20)

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)  #draw buttons rectangle
        for i, line in enumerate(self.text_lines):
            button_text = self.font.render(line, True, (255, 255, 255))
            text_x = self.rect.x + (self.rect.width - button_text.get_width()) // 2
            text_y = self.rect.y + (self.rect.height - (len(self.text_lines) * self.font.get_height())) // 2 + i * self.font.get_height()
            screen.blit(button_text, (text_x, text_y))

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()  # call action if button is clicked (fix so it's connected to keyboard)
    

# button action functions
def edit_game():
    print("Edit Game clicked!")

def game_parameters():
    print("Game Parameters clicked!")

# Countdown variables
##############################
action = False
##############################
countdown_active = False
countdown_time = 30  # 30 seconds countdown
start_ticks = 0  # tracks when countdown started

def start_game():
    print("Start Game clicked!")
    global countdown_active, start_ticks
    countdown_active = True  # Start the countdown
    start_ticks = pygame.time.get_ticks()  # Get the current time in milliseconds
    print("Countdown started!")

def pre_entered_games():
    print("PreEntered Games clicked!")
    #########################
    global action
    action = not action
    init_timer()
    print("Action Display")
    #########################

def view_game():
    print("View Game clicked!")

def flick_sync():
    print("Flick Sync clicked!")

def clear_game():
    print("Clear Game clicked!")
    global tables
    for table in tables:
        for row in table:
            for text_box in row:
                text_box.text = ""

def handle_box_click(row, col):
    global selected_row, selected_col
    selected_row = row
    selected_col = col

# Function to handle a pop-up screen to enter codename when one is not found
def prompt_codename(player_id):
    input_active = True
    codename_textbox = TextBox(300,200,400,40)
   

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            codename_textbox.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # When Enter is pressed, end the input
                    codename = codename_textbox.text
                    input_active = False
                    if codename:
                        insert_player(player_id, codename)
                        input_active = False
                        print(f"Codename entered: {codename}")
                    else:
                        print("Codename can't be empty")
                
        screen.fill((255,255,255))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Enter Codename for Player ID {player_id}:", True, (0,0,0))
        screen.blit(text, (300, 150))
        codename_textbox.draw(screen)
        pygame.display.update()

def add_player():
    global active_table_id
    if selected_row is None or selected_col is None:
        print("No row/column selected")
        return

    # Determine which table (0: left side, 1: right side)
    if active_table_id == 0:
        player_id_text = table1[selected_row][0].text
        equipment_code_text = table1[selected_row][1].text
        team = "Red"
    else:
        player_id_text = table2[selected_row][0].text
        equipment_code_text = table2[selected_row][1].text
        team = "Green"

    # Ensure both fields are filled before converting to the appropriate types
    if not player_id_text or not equipment_code_text:
        print("Player ID or Equipment Code cannot be empty.")
        return

    player_id = player_id_text.strip()  # Keep as a string for varchar storage
    equipment_code = equipment_code_text.strip()

    # Search for an existing codename in the database
    code_name = query_codename(player_id)

    # If no codename is found, prompt for a new one
    if not code_name:
        print(f"Codename not found for Player ID: {player_id}")
        prompt_codename(player_id)  # This will insert the codename into the database if provided

    # Confirm that a codename exists after prompting
    code_name = query_codename(player_id)
    if code_name:
        # Insert the player into the database (for Table 2 as well)
        insert_player(player_id, code_name)

        print(f"Player added:\nTeam: {team}\nName: {code_name}\nID: {player_id}\nEquipment Code: {equipment_code}")

        # Broadcast the equipment code via UDP
        send_equipment_code(equipment_code)
    else:
        print("No codename entered; player was not added.")
    add_player_to_team(team, code_name, score=0)

def add_player_to_team(team, player_name, score=0):
    if team == "Red":
        red_team.append((player_name, score))
    elif team == "Green":
        green_team.append((player_name, score))
    

def delete_player():
    playID = input('ID of player to remove?:')
    remove_player(playID)
    print(f'Player {playID} removed!')

def end_game():
    for _ in range(3):
        send_message("221")
        time.sleep(0.1)
    bye_data()	
    pygame.quit()
    # udp_socket.close()
    sys.exit()

game_start_time = pygame.time.get_ticks()
game_time = pygame.time.get_ticks()
total_game_time = 6 * 60

def increment_score(player_name, points):
    print('points added')
def decrement_score(player_name, points):
    print("points recreased")


def draw_action_screen():
    screen.fill((0, 0, 0))  # Black background

    # Fonts
    font_title = pygame.font.Font(None, 48)
    font_text = pygame.font.Font(None, 36)
  
    # Colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    # Draw the current scores header
    current_scores_header = font_title.render("Current Scores", True, BLUE)
    screen.blit(current_scores_header, (750, 20))

    # Draw Red Team scores
    red_team_header = font_text.render("Red Team", True, RED)
    screen.blit(red_team_header, (50, 20))
    for i, (player, score) in enumerate(red_team):
        player_text = font_text.render(f"{player}: {score}", True, WHITE)
        screen.blit(player_text, (50, 60 + i * 30))

    # Draw Green Team scores
    green_team_header = font_text.render("Green Team", True, GREEN)
    screen.blit(green_team_header, (500, 20))
    for i, (player, score) in enumerate(green_team):
        player_text = font_text.render(f"{player}: {score}", True, WHITE)
        screen.blit(player_text, (500, 60 + i * 30))

    # Draw the action log header
    action_header = font_title.render("Current Game Action", True, BLUE)
    screen.blit(action_header, (50, 200))
     # Draw action log
    y_offset = 150
    for action in reversed(action_log[-10:]):  # Show the last 10 actions
        action_text = font.render(action, True, (255, 255, 255))
        screen.blit(action_text, (50, y_offset))
        y_offset += 30

    pygame.display.update()

    # Timer logic (Update this part)
def init_timer():
	global game_start_time
	game_start_time = pygame.time.get_ticks()
def game_timer():
    elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000  # Elapsed time in seconds
    remaining_time = total_game_time - elapsed_time

    if remaining_time > 0:
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = f"{minutes:02}:{seconds:02}"
    else:
        timer_text = "00:00"  # Show "00:00" when time is up

    # Display the timer on the screen
    font_text = pygame.font.Font(None, 36)
    WHITE = (255,255,255)
    timer_display = font_text.render(timer_text, True, WHITE)
    screen.blit(timer_display, (400, 500))  # Place the timer in the bottom middle

    pygame.display.flip()

    if remaining_time <= 0:
        # Trigger an action when time runs out
        print("6-minute timer has expired!")
        # You may want to end the game or trigger another action here


def test_func():
# usable with 't' for now just used to view table players
    view_database()

button_width = 100  # width 
button_height = 60  # height
button_margin = 10  # margin
y_position = SCREEN_HEIGHT - button_height - 80  # Y-position

buttons = [
    Button("F1\nEdit Game", button_margin + 0 * (button_width + button_margin), y_position, button_width, button_height, edit_game),
    Button("F2\nGame\nParameters", button_margin + 1 * (button_width + button_margin), y_position, button_width, button_height, game_parameters),
    Button("F3\nStart Game", button_margin + 2 * (button_width + button_margin), y_position, button_width, button_height, start_game),
    Button("F5\nAction Screen", button_margin + 3 * (button_width + button_margin), y_position, button_width, button_height, pre_entered_games),
    Button("F7\nAdd\nPlayer", button_margin + 4 * (button_width + button_margin), y_position, button_width, button_height, add_player),
    Button("F8\nView Game", button_margin + 5 * (button_width + button_margin), y_position, button_width, button_height, view_game),
    Button("F10\nFlick Sync", button_margin + 6 * (button_width + button_margin), y_position, button_width, button_height, flick_sync),
    Button("F12\nClear Game", button_margin + 7 * (button_width + button_margin), y_position, button_width, button_height, clear_game),
]

# dictionary to map keys to actions
key_to_action = {
    pygame.K_F1: edit_game,
    pygame.K_F2: game_parameters,
    pygame.K_F3: start_game,
    pygame.K_F5: pre_entered_games,
    pygame.K_F7: add_player,  # no action assigned for F7 yet
    pygame.K_F8: view_game,
    pygame.K_F10: flick_sync,
    pygame.K_F12: clear_game,
    #pygame.K_BACKSPACE: delete_player,
    pygame.K_ESCAPE: end_game,
    pygame.K_F6: test_func
}

# main loop
running = True
on_splash_screen = True
entry_screen_active = True
play_action = True

# Start the update listener thread
listener_thread = threading.Thread(target=listen_for_updates, daemon=True)
listener_thread.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == show_main_screen_event and on_splash_screen:
            on_splash_screen = False
            
        # check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for button in buttons:
                button.is_clicked(mouse_pos)
            for table in tables:
                for row in table:
                    for text_box in row:
                        clicked = text_box.is_clicked(mouse_pos)
                        if clicked is not None:
                            active_table_id, row, col = clicked
                            handle_box_click(row, col)
                            # text_box.active = True
                
        # check for keypress events
        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_action:
                key_to_action[event.key]()
        
        # Handle events for text boxes in the tables
        for table in tables:
            for row in table:
                for text_box in row:
                    text_box.handle_event(event)


    if on_splash_screen:
        # display the splash screen with image
        screen.fill((0, 0, 0))
        screen.blit(logo, ((SCREEN_WIDTH - logo.get_width()) // 2, 50))
        pygame.display.update()
    elif countdown_active:
        # Handle the countdown
        entry_screen_active = False
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        countdown_left = max(countdown_time - seconds_passed, 0)

        # Display countdown
        screen.fill((255, 255, 255))  # White background
        font = pygame.font.Font(None, 100)
        countdown_text = font.render(str(countdown_left), True, (0, 0, 0))  # Black countdown
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()

        if countdown_left <= 0:
            send_message("202")
            print("Countdown ended")
            countdown_active = False
            play_action = True

    #########################################################################
    elif action:
        entry_screen_active = not entry_screen_active
        action = False
        play_action = True
        pygame.display.update()       
    ##########################################################################   
    
    elif entry_screen_active:
        # draw buttons screen
        screen.fill((255, 255, 255))
        ###################################################
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        pygame.display.set_caption("Entry Terminal")
        font = pygame.font.Font(None, 36)
        text = font.render("Edit Current Game",True, BLACK)
        screen.blit(text, (280, 0))
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 550, 800, 40))
        text = font.render("<Del> to Delete Player, <i> to Insert Player or Edit Codename", True, WHITE)
        screen.blit(text, (50,560))
        ##################################################
        
        # Draw the tables
        for table in tables:
            for row in table:
                for text_box in row:
                    text_box.draw(screen)
                    
        #draw columu labels (left)
        label_font = pygame.font.Font(None, 24)
        name_label = label_font.render("ID", True, BLACK)
        id_label = label_font.render("Name", True, BLACK)
        screen.blit(name_label, (100, 30))
        screen.blit(id_label, (200, 30)) 
        # draw column labels (right)
        screen.blit(name_label, (450, 30)) 
        screen.blit(id_label, (550, 30))
                    
        for button in buttons:
            button.draw()
        pygame.display.update()

    # game action screen
    elif play_action:
            draw_action_screen()
            game_timer()

end_game()
