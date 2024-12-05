import pygame
import sys
import socket
import random
import subprocess
import threading
import time
from database import *
from music import Music
from server import Server
from textScroll import TextScroll

player_names = {}

# initializing pygame
pygame.init()
pygame.mixer.init()
server = Server(player_names)
music = Music()


# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the area for the action log (e.g., bottom right corner)
action_log_area = pygame.Rect(50, 250, 900, 180)  # Adjust size and position as needed
font_action_log = pygame.font.Font(None, 24)  # Use a readable font size

action_log_display = TextScroll(
    area=action_log_area,
    font=font_action_log,
    fg_color = WHITE,
    bk_color = BLACK,
    text=[],  # Start with an empty log
    ms_per_line = 2000  # Time delay for each line
)

server.action_log = action_log_display

# set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Splash Screen")

# load and display the splash image
try:
    music.load_track("Track03.mp3")
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (800, 500))
except Exception as error:
    print(f"Error in Splash Screen: {error}")
    pygame.quit()
    sys.exit()

music.play_track(start=120)
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

def receive_message():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            #udp_socket.bind(('127.0.0.1', RECEIVE_PORT))
            data, _ = udp_socket.recvfrom(1024)
            print(f"Received message: {data.decode(FORMAT)}")  # Debug print
            return data.decode(FORMAT)
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

def process_game_event(message):
    global action_log_display

    if message is None:
        print("[ERROR] Received None message, skipping event processing.")
        return

    if "hit Green Base!" in message:
        print(f"[BASE HIT] {message}")
        action_log_display.add_line(message)
        update_score("Green", 100)
    elif "hit Red Base!" in message:
        print(f"[BASE HIT] {message}")
        action_log_display.add_line(message)
        update_score("Red", 100)
    elif ":" in message:
        try:
            transmit_id, hit_id = message.split(":")
            action_log_display.add_line(f"Player {transmit_id} hit Player {hit_id}")
            update_score("Red" if int(transmit_id) % 2 != 0 else "Green", 10)
        except ValueError as e:
            print(f"[ERROR] Unable to parse hit event: {e}")
    else:
        print(f"[UNKNOWN EVENT] Received: {message}")
        action_log_display.add_line(f"Unknown Event: {message}")


    

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

update_thread = threading.Thread(target=listen_for_updates, daemon=True)
update_thread.start()


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
            if event.button == 4:  # Scroll up
                action_log_display.scroll(-1)
            elif event.button == 5:  # Scroll down
                action_log_display.scroll(1)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
            if event.key == pygame.K_UP:  # Arrow up
                action_log_display.scroll(-1)
            elif event.key == pygame.K_DOWN:  # Arrow down
                action_log_display.scroll(1)

    
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
    def __init__(self, text, x, y, width, height, action=None,color=(0, 0, 0), text_color=(255, 255, 255)):
        self.text_lines = text.split('\n')
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.font = pygame.font.Font(None, 20)
        self.color = color 
        self.text_color = text_color


    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)  #draw buttons rectangle
        for i, line in enumerate(self.text_lines):
            button_text = self.font.render(line, True, self.text_color)
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

end_game_button = Button(
    text="End Game",
    x=SCREEN_WIDTH - 150,  # Positioned near the right edge
    y=SCREEN_HEIGHT - 100,  # Positioned near the bottom
    width=120,
    height=40,
    action=None,  # No action needed for now
    color=(255, 255, 255),  # White background
    text_color=(0, 0, 0)  # Black text
)
action_screen_buttons = [end_game_button]


# Countdown variables
action = False
start_count = False

def start_game():
    print("Start Game clicked!")
    global start_count
    init_timer(0.5)
    start_count = True
    
    # music stuff
    music.stop_track()
    music.load_track("Track01.mp3")  
    music.play_track(start=67)
    print("Countdown started!")

def pre_entered_games():
    print("PreEntered Games clicked!")
    #########################
    global action
    action = not action
    init_timer(6)
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
    add_player_names(code_name, equipment_code)

def add_player_to_team(team, player_name, score=0):
    if team == "Red":
        red_team.append((player_name, score))
    elif team == "Green":
        green_team.append((player_name, score))

def add_player_names(player_name, equipment_code):
    player_names.update({player_names: equipment_code})
    

def delete_player():
    playID = input('ID of player to remove?:')
    remove_player(playID)
    print(f'Player {playID} removed!')


def end_game():
    for _ in range(3):
        send_message("221")
        time.sleep(0.1)
        server.stop()
    bye_data()	
    pygame.quit()
    # udp_socket.close()
    sys.exit()

game_start_time = pygame.time.get_ticks()
game_time = pygame.time.get_ticks()
total_game_time = 0

def increment_score(player_name, points):
    print('points added')
def decrement_score(player_name, points):
    print("points recreased")





def draw_action_screen():
    screen.fill((0, 0, 0))  # Black background
      # Example: Add action log entries for testing
    #action_log_display.add_line("Player 1 hit Player 2")
    #action_log_display.add_line("Player 3 hit Player 4")
    #action_log_display.add_line("Game Started!")
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

    scores = server.get_scores()
    player_points = scores["player_points"]
    team_scores = scores["team_scores"]

    # Draw Red Team scores
    red_team_header = font_text.render(f"Red Team: {team_scores['Red']} points", True, RED)
    screen.blit(red_team_header, (50, 20))
    y_offset = 60
    for player_id, score in player_points.items():
        if player_id % 2 != 0:  # Red team
            player_name = player_names.get(player_id, f"Player {player_id}")
            player_text = font_text.render(f"{player_name}: {score}", True, WHITE)
            screen.blit(player_text, (50, y_offset))
            y_offset += 30
    # for i, (player, score) in enumerate(red_team):
    #     player_text = font_text.render(f"{player}: {score}", True, WHITE)
    #     screen.blit(player_text, (50, 60 + i * 30))

    # Draw Green Team scores
    green_team_header = font_text.render(f"Green Team: {team_scores['Green']} points", True, GREEN)
    screen.blit(green_team_header, (500, 20))
    y_offset = 60
    for player_id, score in player_points.items():
        if player_id % 2 == 0:  # Green team
            player_name = player_names.get(player_id, f"Player {player_id}")
            player_text = font_text.render(f"{player_name}: {score}", True, WHITE)
            screen.blit(player_text, (500, y_offset))
            y_offset += 30
    # for i, (player, score) in enumerate(green_team):
    #     player_text = font_text.render(f"{player}: {score}", True, WHITE)
    #     screen.blit(player_text, (500, 60 + i * 30))

    # Draw the action log header
    action_header = font_title.render("Current Game Action", True, BLUE)
    screen.blit(action_header, (50, 200))


    # Display the action log
    for i, log_entry in enumerate(action_log[-10:]):  # Display the last 10 entries
        log_text = font_text.render(log_entry, True, WHITE)
        screen.blit(log_text, (50, 250 + i * 30))

    #action_log_display.update()
    
    action_log_display.draw(screen)
    # Draw the End Game Button
    for button in action_screen_buttons:
        button.draw()
    pygame.display.flip()

    
    
play_action = True
music_started = False

def init_timer(minutes):
	global game_start_time, total_game_time
	game_start_time = pygame.time.get_ticks()
	total_game_time = minutes * 60
	
def game_timer(type: str):
    elapsed_time = (pygame.time.get_ticks() - game_start_time) // 1000  # Elapsed time in seconds
    remaining_time = total_game_time - elapsed_time
    
    global music_started
    
    if remaining_time > 0:
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = f"{minutes:02}:{seconds:02}"
    elif remaining_time == 16:
            music.stop_track()
            music.load_track("Track08.mp3")  # Track to play at 8 seconds
            music.play_track(start=0)
    else:
        timer_text = "00:00"  # Show "00:00" when time is up

	#screen stuff depending on what timer is called
    if type == 'start':
        screen.fill((255, 255, 255))  # White background
        font = pygame.font.Font(None, 100)
        timer_display = font.render(timer_text, True, (0, 0, 0))  # Black
        screen.blit(timer_display, (SCREEN_WIDTH // 2 - timer_display.get_width() // 2, SCREEN_HEIGHT // 2 - timer_display.get_height() // 2))

    elif type == 'game':
    # Display the timer on the screen
        font = pygame.font.Font(None, 36)
        timer_display = font.render(timer_text, True, (129,133,137)) #grey
        screen.blit(timer_display, (400, 500))  # Place the timer in the bottom middle

    pygame.display.flip()

    if remaining_time <= 0:
        if type == 'game':
            # Trigger an action when time runs out
            print("6-minute timer has expired!")
            # You may want to end the game or trigger another action here
        else:
            global start_count, play_action
            # This is where the white space error was.
            start_count = False
            play_action = True
            send_message("202")
            init_timer(6)

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

# Timer event for updates (e.g., every second)
GAME_UPDATE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GAME_UPDATE_EVENT, 1000)  # Trigger every 1000 ms (1 second)


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
            for button in action_screen_buttons:
                if button.is_clicked(mouse_pos): 
                    print("End Game Button clicked!")
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
    
    elif start_count:
        entry_screen_active = False
        game_timer('start')        
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
        id_label = label_font.render("Equipment ID", True, BLACK)
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
            game_timer('game')

end_game
