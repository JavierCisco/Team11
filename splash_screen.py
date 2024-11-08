# splashScreen.py
import pygame
import sys

def init_splash_screen():
    try:
        splash_sound = pygame.mixer.Sound("theme.mp3")
        logo = pygame.image.load("logo.png").convert_alpha()
        logo = pygame.transform.scale(logo, (800, 500))
        splash_sound.play()
        return logo, splash_sound
    except Exception as error:
        print(f"Error in Splash Screen: {error}")
        pygame.quit()
        sys.exit()

def display_splash_screen(screen, logo):
    screen.fill((0, 0, 0))
    screen.blit(logo, ((screen.get_width() - logo.get_width()) // 2, 50))
    pygame.display.update()