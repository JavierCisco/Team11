import pygame
from database import insert_player, query_codename

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

# Button class
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text_lines = text.split('\n')
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.font = pygame.font.Font(None, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        for i, line in enumerate(self.text_lines):
            button_text = self.font.render(line, True, (255, 255, 255))
            text_x = self.rect.x + (self.rect.width - button_text.get_width()) // 2
            text_y = self.rect.y + (self.rect.height - (len(self.text_lines) * self.font.get_height())) // 2 + i * self.font.get_height()
            screen.blit(button_text, (text_x, text_y))

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

# Create tables of text boxes (2 columns x 10 rows each)
def create_tables():
    table1 = []
    table2 = []
    cell_width = 100
    cell_height = 40

    # Table 1 (left side)
    for row in range(10):
        table_row = []
        for col in range(2):
            x = 100 + col * cell_width
            y = 50 + row * cell_height
            table_row.append(TextBox(x, y, cell_width, cell_height, table_id=0, row=row, col=col))
        table1.append(table_row)

    # Table 2 (right side)
    for row in range(10):
        table_row = []
        for col in range(2):
            x = 450 + col * cell_width
            y = 50 + row * cell_height
            table_row.append(TextBox(x, y, cell_width, cell_height, table_id=1, row=row, col=col))
        table2.append(table_row)

    return [table1, table2]

# Function to handle adding a player
def add_player(tables, selected_row, selected_col, active_table_id):
    if selected_row is None or selected_col is None:
        print("No row/column selected")
        return

    if active_table_id == 0:
        player_id_text = tables[0][selected_row][0].text
        equipment_code_text = tables[0][selected_row][1].text
    else:
        player_id_text = tables[1][selected_row][0].text
        equipment_code_text = tables[1][selected_row][1].text

    if not player_id_text or not equipment_code_text:
        print("Player ID or Equipment Code cannot be empty.")
        return

    player_id = player_id_text
    equipment_code = equipment_code_text

    # Search the database for existing codename
    code_name = query_codename(player_id)

    if not code_name:
        print("Code name not found for player ID:", player_id)
        # Prompt for codename (can be implemented in this file or imported)
        # code_name = prompt_codename(player_id)
        insert_player(player_id, code_name)
        print(f"Player added: {code_name} - ID: {player_id}")
    else:
        print(f"Player found: {code_name} - ID: {player_id}")


