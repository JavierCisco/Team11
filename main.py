import sys
import random
from database import *
from socks import *
from User-Interface import *

# Call functions (from socks.py)  to start the server and client
start_server()
start_client()


def add_player():
    player_id = random.randint(1000, 9999)  # This would be dynamically generated or provided
    send_equipment_code(player_id)
    name = input('Name of player?:')
    insert_player(player_id, name)
    print(f"Added:\nName: {name}\nID: {player_id}")

def delete_player():
    playID = input('ID of player to remove?:')
    remove_player(playID)
    print(f'Player {playID} removed!')

# CHECK AND ADD THE FUNCTIONS TO THEIR RESPECTIVE FILES TO MAKE SURE THEY GET CALLED PROPERLY FOR THE SPECFIC INSTANCE
def end_game():
    bye_data()	
    pygame.quit()
    udp_socket.close()
    sys.exit()

def test_func():
# usable with 't' for now just used to view table players
    view_database()


# main loop
running = True
on_splash_screen = True
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
                
        # check for keypress events
        elif event.type == pygame.KEYDOWN:
            if event.key in key_to_action:
                key_to_action[event.key]()
            # elif event.key == pygame.K_i:
            #     id = int(input("Enter player ID: "))
            #     codename = input("Enter player codename: ").strip()
            #     equipment_code = input(f"Enter equipment code for {codename}: ")
            #     add_player_transmit(id, codename, equipment_code)
        
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
    else:
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

end_game
