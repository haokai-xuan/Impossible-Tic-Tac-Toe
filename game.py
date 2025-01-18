import pygame
import random
import copy

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

def minimax(s, depth, is_max):
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
            v = max(v, minimax(result(s, action), depth + 1, False))
        
        return v
    else:
        v = float('inf')

        for action in actions(s):
            v = min(v, minimax(result(s, action), depth + 1, True))

        return v

def find_best_move(s):
    who_to_move = player(s)
    best_val = float('-inf') if who_to_move == "X" else float('inf')
    best_move = None

    for action in actions(s):
        val = minimax(result(s, action), 0, who_to_move == "O")
        if (who_to_move == "X" and val > best_val) or (who_to_move == "O" and val < best_val):
            best_val = val
            best_move = action

    return best_move

def print_board(state):
    print("-----------")
    for i in range(3):
        for j in range(3):
            print(f"[{state[i][j] if state[i][j] is not None else " "}]", end=" ")
        print("\n")
    print("-----------")

player_turn = random.choice([True, False])
while True:
    print_board(state)
    if player_turn:
        while True:
            r, c = int(input("Row: ")), int(input("Col: "))
            if (r, c) in actions(state):
                state = result(state, (r, c))
                break
            else:
                print("Invalid pos")
    else:
        if all(cell is None for row in state for cell in row):
            state = result(state, random.choice(actions(state)))
        else:
            move = find_best_move(state)
            state = result(state, move)

    player_turn = not player_turn

    if terminal(state):
        print_board(state)
        if utility(state) == 10:
            print("X wins")
        elif utility(state) == -10:
            print("O wins")
        else:
            print("Tie")
        break