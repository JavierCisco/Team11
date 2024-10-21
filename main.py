import pygame
import sys
import socket
import random
import subprocess
from database import *
from action_display import display_action_screen  # Import the action display function

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

# Functions to start the server and client
def start_server():
    subprocess.Popen(['python3', 'server.py'])  # Start the UDP server

def start_client():
    subprocess.Popen(['python3', 'client.py'])  # Start the UDP client

# Call these functions to start the server and client
start_server()
start_client()

# UDP setup
UDP_IP = "127.0.0.1"  # replace with your target IP
UDP_PORT = 7500       # the port to broadcast equipment codes
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_equipment_code(code):
    message = str(code).encode('utf-8')
    udp_socket.sendto(message, (UDP_IP, UDP_PORT))
    print(f"Sent equipment code: {code}")

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
    action = True
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

    if active_table_id == 0:
        player_id_text = table1[selected_row][0].text
        print(f"playerID is {player_id_text}")
        equipment_code_text = table1[selected_row][1].text
    else:
        player_id_text = table2[selected_row][0].text
        print(f"playerIDTable2 is {player_id_text}")
        equipment_code_text = table2[selected_row][1].text

    # Ensure both fields are not empty before converting
    if not player_id_text or not equipment_code_text:
        print("Player ID or Equipment Code cannot be empty.")
        return
    player_id = player_id_text  # Keep as string
    equipment_code = equipment_code_text

    # Search databse for existing codename
    code_name = query_codename(player_id)

    # If no codename found, enter a new codename
    if not code_name:
        print("Code name not found for player ID:", player_id)
        code_name = prompt_codename(player_id)
        if code_name:
            insert_player(player_id, code_name)
            print(f"Player added:\nName: {code_name}\nID: {player_id}")
        else:
            print("No codename entered")
    else:
        print(f"Player found:\nName: {code_name}\nID: {player_id}")

    # while True:
    #     try:
    #         equipment_id = int(input("Enter equipment ID (must be an integer): "))
    #         break
    #     except ValueError:
    #         print("Invalid input. Please enter an integer.")   
    
    # Broadcast equipment code
    send_equipment_code(equipment_code)
    

def delete_player():
    playID = input('ID of player to remove?:')
    remove_player(playID)
    print(f'Player {playID} removed!')

def end_game():
    bye_data()	
    pygame.quit()
    udp_socket.close()
    sys.exit()

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
    Button("F7\nAdd\nPlayer", button_margin + 4 * (button_width + button_margin), y_position, button_width, button_height),
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
    # pygame.K_i: add_player,
    pygame.K_BACKSPACE: delete_player,
    pygame.K_ESCAPE: end_game,
    pygame.K_F6: test_func
}

# main loop
running = True
on_splash_screen = True
entry_screen_active = True
play_action = True

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
            #######################################
            elif event.key == pygame.K_F5:
                action = True
                
            elif event.key == pygame.K_F5:
                clear_game
            #######################################
        
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
            print("Countdown ended")
            countdown_active = False
            play_action = True

    #########################################################################
    elif action:
        entry_screen_active = False
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
        ###################################################
        
        # Draw the tables
        for table in tables:
            for row in table:
                for text_box in row:
                    text_box.draw(screen)
                    
        for button in buttons:
            button.draw()
        pygame.display.update()

    # game action screen
    elif play_action:


        #temporary action log, team scores, and time
            action_log = ["Player A hit Player B", "Player C hit Player D", "Player E hit the base"]
            red_team_score = 5000
            green_team_score = 4500
            game_time_remaining = 60
            # List of players on each team
            red_team_players = ["Player A", "Player B", "Player C"]
            green_team_players = ["Player D", "Player E", "Player F"]

            display_action_screen(screen, action_log, red_team_score, green_team_score, game_time_remaining, red_team_players, green_team_players)


end_game

