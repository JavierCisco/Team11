# countdown.py
import pygame

def countdown(screen, countdown_time=30):
    pygame.init()

    countdown_active = True
    start_ticks = pygame.time.get_ticks()  # tracks when countdown started
    action = False  # Flag to indicate countdown is over

    while countdown_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        countdown_left = max(countdown_time - seconds_passed, 0)

        # Display countdown
        screen.fill((255, 255, 255))  # White background
        font = pygame.font.Font(None, 100)
        countdown_text = font.render(str(countdown_left), True, (0, 0, 0))  # Black countdown
        screen.blit(countdown_text, (screen.get_width() // 2 - countdown_text.get_width() // 2, screen.get_height() // 2 - countdown_text.get_height() // 2))
        pygame.display.update()

        if countdown_left <= 0:
            print("Countdown ended")
            countdown_active = False
            action = True  # This can trigger further actions after the countdown

    return action


