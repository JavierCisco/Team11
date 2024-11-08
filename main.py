import pygame
import sys
from database import *
import subprocess
import socket
from splash_screen import init_splash_screen, display_splash_screen
from countdown import countdown
from entryScreen import Button, TextBox, create_tables, add_player
from action_display import * 

# initializing pygame
pygame.init()
pygame.mixer.init()

# screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption("Splash Screen")

# Initialize splash screen elements
logo, splash_sound = init_splash_screen()

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


# button action functions
def edit_game():
    print("Edit Game clicked!")

def game_parameters():
    print("Game Parameters clicked!")

# Countdown variables
##############################
action = False
countdown_active = False
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

# Create tables and buttons
tables = create_tables()
buttons = [
    Button("F1\nEdit Game", 10, 500, 100, 60, edit_game),
    Button("F2\nGame Parameters", 120, 500, 100, 60, game_parameters),
    Button("F3\nStart Game", 230, 500, 100, 60, start_game),
    Button("F12\nClear Game", 450, 500, 100, 60, clear_game),
    Button("Exit", 560, 500, 100, 60, end_game)
]

# Key to action mapping
key_to_action = {
    pygame.K_F1: edit_game,
    pygame.K_F2: game_parameters,
    pygame.K_F3: start_game,
    pygame.K_F12: clear_game,
    pygame.K_ESCAPE: end_game
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
        
        # Handle events for text boxes in the tables
        for table in tables:
            for row in table:
                for text_box in row:
                    text_box.handle_event(event)


    if on_splash_screen:
        # Display the splash screen with image
        display_splash_screen(screen, logo)

    elif countdown_active:
        action = countdown(screen)  # this will handle the countdown
        if action:
            # Do something after countdown ends, like starting the game or transitioning to another screen
            countdown_active = False

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
        ###################################################
        
        # Draw the tables
        for table in tables:
            for row in table:
                for text_box in row:
                    text_box.draw(screen)
                    
        for button in buttons:
            button.draw(screen)
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
    pygame.display.flip()

end_game

