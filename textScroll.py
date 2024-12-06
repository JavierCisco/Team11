import pygame
import time
import os
import sys

class TextScroll:
    def __init__(self, area, font, fg_color, bk_color, text, ms_per_line):
        self.area = area
        self.font = font
        self.fg_color = fg_color
        self.bk_color = bk_color
        self.text = []
        self.ms_per_line = ms_per_line
        self.last_update_time = pygame.time.get_ticks()
        self.scroll_offset = 0


    def add_line(self, line):
        max_lines = self.area.height // self.font.get_height()  # Calculate visible lines
        self.text.append(line)  # Store as a string

        if len(self.text) > max_lines * 2:  # Limit to double the visible area
            self.text.pop(0)  # Remove the oldest entry

        print(f"[DEBUG] Added to Action Log: {line}")  # Debugging

    def scroll(self, direction):
        lines_visible = self.area.height // self.font.get_height()
        max_offset = max(0, len(self.text) - lines_visible)
        self.scroll_offset = max(0, min(self.scroll_offset + direction, max_offset))

    def draw(self, screen):
        current_time = pygame.time.get_ticks()

        # Remove a line if enough time has passed
        if current_time - self.last_update_time > self.ms_per_line:
            self.last_update_time = current_time
            # Only remove a line if there are more lines than the visible area
            if len(self.text) > self.area.height // self.font.get_height():
                self.text.pop(0)

        # Draw the action log
        pygame.draw.rect(screen, self.bk_color, self.area)
        y_offset = self.area.top

        for line in self.text:
            text_surface = self.font.render(line, True, self.fg_color)
            screen.blit(text_surface, (self.area.left, y_offset))
            y_offset += text_surface.get_height()

        pygame.display.update()



