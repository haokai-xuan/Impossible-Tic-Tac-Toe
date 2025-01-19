import pygame
import random
import copy

pygame.init()

width = 600
height = 600
screen = pygame.display.set_mode((width, height))
font = pygame.font.Font("assets/TicTacToe.ttf", 100)
title_font = pygame.font.Font("assets/TicTacToe.ttf", 50)
icon = pygame.image.load("assets/game.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Impossible Tic Tac Toe")

bg_img = pygame.image.load("assets/bg.png")
x_img = pygame.image.load("assets/x.png")
o_img = pygame.image.load("assets/o.png")

piece_icon = {"X": x_img, "O": o_img}

player_turn = random.choice([True, False])
current_screen = "menu"
FPS = 30
clock = pygame.time.Clock()
ai_delay_time = 0.75 # Number of seconds to wait after player's move
curr_ai_delay_time = 0

class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Hover
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True
        
        return False
    
play_again_button = Button(225, 300, 150, 50, (204, 204, 204), (230, 230, 230), "Menu", (0, 0, 0), title_font)
quit_button = Button(225, 360, 150, 50, (204, 204, 204), (230, 230, 230), "Quit", (0, 0, 0), title_font)
x_button = Button(225, 240, 150, 50, (255, 84, 64), (230, 60, 45), "X", (0, 0, 0), title_font)
o_button = Button(225, 300, 150, 50, (93, 121, 188), (72, 100, 168), "O", (0, 0, 0), title_font)

# Initial state
state = [[None for _ in range(3)] for _ in range(3)]

# Returns which player to move in state s
def player(s):
    x_count = sum(row.count("X") for row in s)
    o_count = sum(row.count("O") for row in s)

    return "X" if x_count <= o_count else "O"

# Returns legal moves in state s
def actions(s):
    legal_actions = []
    for i in range(3):
        for j in range(3):
            if s[i][j] is None:
                legal_actions.append((i, j))

    return legal_actions

# Returns state after action a taken in state s
def result(s, a):
    p = player(s)

    row, col = a

    new_state = copy.deepcopy(s)

    new_state[row][col] = p
    
    return new_state

# Checks if state s is terminal state
def terminal(s):
    # Check win row/col
    for i in range(3):
        if s[i][0] == s[i][1] == s[i][2] and s[i][0] is not None:
            return True
        if s[0][i] == s[1][i] == s[2][i] and s[0][i] is not None:
            return True
        
    # Check diagonal
    if s[0][0] == s[1][1] == s[2][2] and s[0][0] is not None:
        return True
    if s[2][0] == s[1][1] == s[0][2] and s[2][0] is not None:
        return True

    # Check boar full
    for row in s:
        if None in row:
            return False

    return True

# Final numerical value for terminal state s
def utility(s):
    # Check win row/col
    for i in range(3):
        if s[i][0] == s[i][1] == s[i][2] and s[i][0] is not None:
            return 10 if s[i][0] == "X" else -10
        if s[0][i] == s[1][i] == s[2][i] and s[0][i] is not None:
            return 10 if s[0][i] == "X" else -10
        
    # Check diagonal
    if s[0][0] == s[1][1] == s[2][2] and s[0][0] is not None:
        return 10 if s[0][0] == "X" else -10
    if s[2][0] == s[1][1] == s[0][2] and s[2][0] is not None:
        return 10 if s[2][0] == "X" else -10
    
    return 0

# alpha is the maximum value that the maximizing player can get so far
# beta is the minimum value that the minimizing player can get so far
def minimax(s, depth, alpha, beta, is_max):
    if terminal(s):
        win_val = utility(s)
        if win_val == 10:
            return 10 - depth
        elif win_val == -10:
            return -10 + depth
        else:
            return 0
    
    if is_max:
        v = float('-inf')

        for action in actions(s):
            v = max(v, minimax(result(s, action), depth + 1, alpha, beta, False))
            if v > beta:
                break
            alpha = max(v, alpha)
        
        return v
    else:
        v = float('inf')

        for action in actions(s):
            v = min(v, minimax(result(s, action), depth + 1, alpha, beta, True))
            if v < alpha:
                break
            beta = min(v, beta)

        return v

def find_best_move(s):
    who_to_move = player(s)
    best_val = float('-inf') if who_to_move == "X" else float('inf')
    best_move = None

    for action in actions(s):
        val = minimax(result(s, action), 0, float('-inf'), float('inf'), who_to_move == "O")
        if (who_to_move == "X" and val > best_val) or (who_to_move == "O" and val < best_val):
            best_val = val
            best_move = action

    return best_move

def get_action(pos):
    row, col = pos[1] // (height // 3), pos[0] // (width // 3)
    return row, col

def draw_state():
    for i in range(3):
        for j in range(3):
            if state[i][j] is not None:
                screen.blit(piece_icon[state[i][j]], (j * width // 3 + 36,
                                                      i * height // 3 + 36))

def draw_board():
    screen.blit(bg_img, (0, 0))

    for i in range(1, 3):
        pygame.draw.line(screen, (0, 0, 0), ((width // 3) * i, 0), ((width // 3) * i, height), 5)
        pygame.draw.line(screen, (0, 0, 0), (0, (height // 3) * i), (width, (height // 3) * i), 5)                

def draw_overlay():
    overlay = pygame.Surface((600, 600), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 192))
    screen.blit(overlay, (0, 0))

def draw_menu():
    global current_screen, player_turn
    draw_board()
    draw_overlay()

    text = title_font.render("Impossible Tic Tac Toe", True, (0, 0, 0))
    screen.blit(text, ((width - text.get_size()[0]) // 2,
                       150))
    
    x_button.draw(screen)
    o_button.draw(screen)
    quit_button.draw(screen)

    for event in pygame.event.get():
        if x_button.is_clicked(event):
            player_turn = True
            current_screen = "game"
        elif o_button.is_clicked(event):
            player_turn = False
            current_screen = "game"
        elif quit_button.is_clicked(event) or event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
def draw_end():
    global current_screen, state

    draw_board()
    draw_state()

    text = None
    draw_overlay()

    if utility(state) == 10:
        text = font.render("X Wins!", True, (0, 0, 0))
        # print("X wins")
    elif utility(state) == -10:
        text = font.render("O Wins!", True, (0, 0, 0))
        # print("O wins")
    else:
        text = font.render("Tie!", True, (0, 0, 0))
        # print("Tie")
    
    screen.blit(text, ((width - text.get_size()[0]) // 2,
                    200))
    
    play_again_button.draw(screen)
    quit_button.draw(screen)
    for event in pygame.event.get():
        if play_again_button.is_clicked(event):
            current_screen = "menu"
            state = [[None for _ in range(3)] for _ in range(3)]
        if quit_button.is_clicked(event) or event.type == pygame.QUIT:
            pygame.quit()
            exit()

def draw_game():
    global current_screen, state, player_turn, curr_ai_delay_time
    
    if not player_turn:
        curr_ai_delay_time += 1 / (ai_delay_time * FPS)

    draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if player_turn:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                r, c = get_action(pos)
                if (r, c) in actions(state):
                    state = result(state, (r, c))
                    player_turn = not player_turn
                    # print_board(state)

    if not player_turn and curr_ai_delay_time >= ai_delay_time:
        curr_ai_delay_time = 0
        if all(cell is None for row in state for cell in row):
            state = result(state, random.choice(actions(state)))
        else:
            move = find_best_move(state)
            if move:
                state = result(state, move)

        player_turn = not player_turn
        # print_board(state)
    
    draw_state()

    if terminal(state):
        current_screen = "end"

'''  
def print_board(state):
    print("-----------")
    for i in range(3):
        for j in range(3):
            print(f"[{state[i][j] if state[i][j] is not None else " "}]", end=" ")
        print("\n")
    print("-----------")
'''

while True:
    clock.tick(FPS)

    if current_screen == "menu":
        draw_menu()

    elif current_screen== "game":
        draw_game()

    elif current_screen == "end":
        draw_end()

    pygame.display.update()