import pygame

def display_action_screen(screen, action_log, red_team_score, green_team_score, game_time_remaining, red_team_players, green_team_players):
    """Display the action screen with team scores and player names"""
    screen.fill((0, 0, 0))
    
   
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    
    font = pygame.font.Font(None, 36)

   
    red_team_text = font.render("RED TEAM", True, RED)
    red_team_score_text = font.render(str(red_team_score), True, RED)
    screen.blit(red_team_text, (50, 50))
    screen.blit(red_team_score_text, (50, 100))
    
   
    for idx, player in enumerate(red_team_players):
        player_text = font.render(player, True, RED)
        screen.blit(player_text, (50, 150 + idx * 30))  # Spacing between player names

    
    green_team_text = font.render("GREEN TEAM", True, GREEN)
    green_team_score_text = font.render(str(green_team_score), True, GREEN)
    screen.blit(green_team_text, (500, 50))
    screen.blit(green_team_score_text, (500, 100))
    
    
    for idx, player in enumerate(green_team_players):
        player_text = font.render(player, True, GREEN)
        screen.blit(player_text, (500, 150 + idx * 30))  # Spacing between player names

    pygame.display.update()
