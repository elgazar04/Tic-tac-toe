import tkinter as tk
from tkinter import *
import math

# Constants for representing the players and empty cells
EMPTY = "-"
PLAYER_X = "X"
PLAYER_O = "O"

# The game board
board = [EMPTY] * 9

# Variable to track the current player
current_player = PLAYER_O  # Start with PLAYER_O (human)
ai_strategy = "minimax"  # Default AI strategy

#images for buttons
images = {}

# Function to move the window by dragging
def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')


# Function to print the board in matrix format
def print_board(board, msg=""):
    if msg:
        print(f"\n{msg}")
    print("Current Board:")
    for i in range(0, 9, 3):
        print(f"  {board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6:
            print(" ---+---+---")
    print()  # Blank line for separation

# Function to check if a player has won
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]

    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != EMPTY:
            print(f"Winner found: {board[combination[0]]} wins with combination {combination}!")
            return board[combination[0]]

    if EMPTY not in board:
        print("It's a tie! No empty spaces left.")
        return "tie"

    return None

# Function to evaluate the game board
def evaluate(board):
    winner = check_winner(board)
    if winner == PLAYER_X:
        return 1
    elif winner == PLAYER_O:
        return -1
    else:
        return 0

# Function to rotate the board 90 degrees
def rotate_90(board):
    rotated = [board[6], board[3], board[0],
               board[7], board[4], board[1],
               board[8], board[5], board[2]]
    print_board(rotated, "Rotated Board (90 degrees):")
    return rotated

# Function to reflect the board horizontally
def reflect_horizontal(board):
    reflected = [board[2], board[1], board[0],
                 board[5], board[4], board[3],
                 board[8], board[7], board[6]]
    print_board(reflected, "Reflected Board (Horizontally):")
    return reflected

# Function to generate all symmetric board configurations
def get_symmetries(board):
    symmetries = []
    rotated_board = board
    for i in range(4):  # Rotate the board 90 degrees four times (0, 90, 180, 270)
        rotated_board = rotate_90(rotated_board)
        symmetries.append(rotated_board)
        reflected_rotated = reflect_horizontal(rotated_board)
        symmetries.append(reflected_rotated)
    print(f"Generated {len(symmetries)} symmetric board configurations.")
    return symmetries

# Standard Minimax algorithm
def minimax(board, depth, is_maximizing_player):
    print_board(board, f"Minimax at Depth {depth} ({'Maximizing' if is_maximizing_player else 'Minimizing'})")
    winner = check_winner(board)
    if winner == PLAYER_X:
        return 10 - depth
    elif winner == PLAYER_O:
        return depth - 10
    elif EMPTY not in board:
        return 0

    if is_maximizing_player:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_X
                eval_score = minimax(board, depth + 1, False)
                board[i] = EMPTY
                max_eval = max(max_eval, eval_score)
        print(f"Maximizing player: Best value = {max_eval} at depth {depth}")
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_O
                eval_score = minimax(board, depth + 1, True)
                board[i] = EMPTY
                min_eval = min(min_eval, eval_score)
        print(f"Minimizing player: Best value = {min_eval} at depth {depth}")
        return min_eval

# Minimax function with alpha-beta pruning
def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    print_board(board, f"Alpha-Beta at Depth {depth} (Alpha: {alpha}, Beta: {beta})")
    winner = check_winner(board)
    if winner == PLAYER_X:
        return 10 - depth
    elif winner == PLAYER_O:
        return depth - 10
    elif EMPTY not in board:
        return 0

    if maximizing_player:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_X
                eval_score = minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                board[i] = EMPTY
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    print(f"Pruning at depth {depth}: Alpha = {alpha}, Beta = {beta}")
                    break
        print(f"Maximizing player: Best value = {max_eval} at depth {depth}")
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_O
                eval_score = minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                board[i] = EMPTY
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    print(f"Pruning at depth {depth}: Alpha = {alpha}, Beta = {beta}")
                    break
        print(f"Minimizing player: Best value = {min_eval} at depth {depth}")
        return min_eval

# Minimax with heuristic and symmetry reduction
def heuristic_minimax(board, depth, is_maximizing_player, heuristic=None, explored_boards=None):
    if explored_boards is None:
        explored_boards = {}

    print_board(board, f"Heuristic Minimax at Depth {depth} ({'Maximizing' if is_maximizing_player else 'Minimizing'})")

    winner = check_winner(board)
    if winner == PLAYER_X:
        return 10 - depth
    elif winner == PLAYER_O:
        return depth - 10
    elif EMPTY not in board:
        return 0

    if depth == 0:
        return evaluate(board)

    # Generate canonical form of the board to handle symmetry
    canonical_form = min(tuple(board), *map(tuple, get_symmetries(board)))

    # If this board (or any of its symmetries) has been explored before, return the stored value
    if canonical_form in explored_boards:
        print(f"Using stored evaluation for canonical board: {canonical_form}")
        return explored_boards[canonical_form]

    if is_maximizing_player:
        max_eval = -math.inf
        possible_moves = heuristic(board, PLAYER_X) if heuristic else [i for i in range(9) if board[i] == EMPTY]
        print(f"Maximizing player possible moves: {possible_moves}")
        for move in possible_moves:
            board[move] = PLAYER_X
            eval_score = heuristic_minimax(board, depth - 1, False, heuristic, explored_boards)
            board[move] = EMPTY
            max_eval = max(max_eval, eval_score)
        explored_boards[canonical_form] = max_eval  # Store the evaluated value for this canonical form
        print(f"Maximizing player: Best value = {max_eval} at depth {depth}")
        return max_eval
    else:
        min_eval = math.inf
        possible_moves = heuristic(board, PLAYER_O) if heuristic else [i for i in range(9) if board[i] == EMPTY]
        print(f"Minimizing player possible moves: {possible_moves}")
        for move in possible_moves:
            board[move] = PLAYER_O
            eval_score = heuristic_minimax(board, depth - 1, True, heuristic, explored_boards)
            board[move] = EMPTY
            min_eval = min(min_eval, eval_score)
        explored_boards[canonical_form] = min_eval  # Store the evaluated value for this canonical form
        print(f"Minimizing player: Best value = {min_eval} at depth {depth}")
        return min_eval

# Heuristic 1: Immediate Win or Block with Heuristic Center and Corners
def heuristic_immediate_win_or_block(board, player):
    opponent = PLAYER_X if player == PLAYER_O else PLAYER_O
    for combo in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]:
        values = [board[i] for i in combo]
        if values.count(player) == 2 and values.count(EMPTY) == 1:
            move = combo[values.index(EMPTY)]
            print(f"Found immediate win or block: moving to{move}.")
            return [move]
        if values.count(opponent) == 2 and values.count(EMPTY) == 1:
            move = combo[values.index(EMPTY)]
            print(f"Found immediate win or block: moving to{move}.")
            return [move]
    print(f"Didn't find immediate wins or blocks, defaulting to available moves.")
    return [i for i in range(9) if board[i] == EMPTY]  # Default to available moves if no immediate win or block
        
# Heuristic 2: Heuristic Center and Corners
def heuristic_center_and_corners(board, player):
    if board[4] == EMPTY:
        print("Center is empty, moving to the center.")
        return [4]  # Take center if available
    moves = [i for i in [0, 2, 6, 8] if board[i] == EMPTY]
    print(f"Center is taken. Available corners: {moves}")
    return moves if moves else [i for i in range(9) if board[i] == EMPTY]  # Fallback to any empty spot

# Function to switch the current player
def switch_player():
    global current_player
    current_player = PLAYER_X if current_player == PLAYER_O else PLAYER_O
    print(f"Switched player: Now it's {current_player}'s turn.")
    update_status("amove")

# Function to make a move on the board
def make_move(index, player):
    if board[index] == EMPTY:
        board[index] = player
        print_board(board, f"{player} made a move at position {index}")
        return True
    else:
        print(f"Invalid move at position {index}. Cell already occupied.")
    return False

# Function to get the best move for the AI
def get_best_move():
    best_move = None
    best_value = -math.inf
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = PLAYER_X
            if ai_strategy == "minimax":
                move_value = minimax(board, 0, False)
            elif ai_strategy == "alpha-beta":
                move_value = minimax_alpha_beta(board, 0, -math.inf, math.inf, False)
            elif ai_strategy == "heuristic_minimax_1":
                move_value = heuristic_minimax(board, 3, False, heuristic_immediate_win_or_block)
            elif ai_strategy == "heuristic_minimax_2":
                move_value = heuristic_minimax(board, 3, False, heuristic_center_and_corners)

            board[i] = EMPTY

            print(f"Evaluated move at {i}: Value = {move_value}")
            if move_value > best_value:
                best_value = move_value
                best_move = i

    print(f"Best move for AI: Position {best_move} with value {best_value}\n" + "-"*30)
    return best_move

# Function to reset the game
def reset_game():
    global board, current_player
    board = [EMPTY] * 9
    current_player = PLAYER_O  # Start with PLAYER_O (human)
    for i in range(9):
        buttons[i].config(image=images["play"])
        buttons[i]["state"] = tk.NORMAL
    update_status("amove")
    print_board(board, "Game reset!")

# Function to update the game status and player turn image
def update_status(message):
    status_label.config(text=message)
    if message == "o":
        status_label.config(image=images["o_turn"])
    elif message == "x":
        status_label.config(image=images["x_turn"])
    elif message == "amove":
        status_label.config(image=images["amove"])
    else:
        status_label.config(image=images["tie"])


# Function to handle button click (human move)
def on_button_click(index):
    global current_player
    if make_move(index, current_player):
        buttons[index].config(image=images[current_player.lower()])
        winner = check_winner(board)
        if winner:
            if winner == "tie":
                update_status("tie")
            else:
                update_status(f"{winner.lower()}")
            for btn in buttons:
                btn["state"] = tk.DISABLED
        else:
            switch_player()
            if current_player == PLAYER_X:  # AI's turn
                ai_move = get_best_move()
                if ai_move is not None:
                    make_move(ai_move, current_player)
                    buttons[ai_move].config(image=images[current_player.lower()])
                    winner = check_winner(board)
                    if winner:
                        if winner == "tie":
                            update_status("tie")
                        else:
                            update_status(f"{winner.lower()}")
                        for btn in buttons:
                            btn["state"] = tk.DISABLED
                    else:
                        switch_player()


# Function to set AI strategy
def set_ai_strategy(strategy):
    global ai_strategy
    ai_strategy = strategy
    reset_game()
    
    # Update button images for selection highlight
    minimax_button.config(image=images["minimax" if strategy != "minimax" else "minimax-s"])
    ab_button.config(image=images["alpha_beta" if strategy != "alpha-beta" else "alpha_beta_s"])
    h1_button.config(image=images["heuristic_1" if strategy != "heuristic_minimax_1" else "heuristic_1_s"])
    h2_button.config(image=images["heuristic_2" if strategy != "heuristic_minimax_2" else "heuristic_2_s"])

    print(f"AI Strategy set to: {ai_strategy}\n" + "="*30)


# Tkinter GUI setup
root = tk.Tk()
root.overrideredirect(1)  # Remove window decorations
root.bind("<B1-Motion>", move_window)  # Enable window dragging
images["bg"] = PhotoImage(file="Board.png")
canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack(fill=BOTH, expand=1)
canvas.create_image(0, 0, image=images["bg"], anchor="nw")
# Load button images and store them in the global dictionary
images["minimax"] = PhotoImage(file="minimax.png")
images["minimax-s"] = PhotoImage(file="minimax-s.png")
images["alpha_beta"] = PhotoImage(file="ab.png")
images["alpha_beta_s"] = PhotoImage(file="ab-s.png")
images["heuristic_1"] = PhotoImage(file="h.png")
images["heuristic_1_s"] = PhotoImage(file="h-s.png")
images["heuristic_2"] = PhotoImage(file="h2.png")
images["heuristic_2_s"] = PhotoImage(file="h2-s.png")
images["play"] = PhotoImage(file="play.png")
images["x"]= PhotoImage(file="x.png")
images["o"]= PhotoImage(file="o.png")
images["amove"]= PhotoImage(file="amove.png")
images["o_turn"]= PhotoImage(file="o_turn.png")
images["x_turn"]= PhotoImage(file="x_turn.png")
images["tie"]= PhotoImage(file="tie.png")
images["reset"]= PhotoImage(file="reset.png")
images["exit"] = PhotoImage(file="exit.png")
#######################
minimage = PhotoImage(file="minimax.png")
minimax_button = tk.Button(root, text="", command=lambda: set_ai_strategy("minimax"), font=("Arial", 12), fg="#5A1E76", bg="#5A1E76", activebackground="#5A1E76", activeforeground="#5A1E76", borderwidth=0, highlightthickness = 0, bd = 0, cursor="hand1")
minimax_button.config(image=images["minimax"])
minimax_button.place(x=980, y=85, width=214, height=111)
########################
abimage = PhotoImage(file="ab.png")
ab_button = tk.Button(root, text="", command=lambda: set_ai_strategy("alpha-beta"), font=("Arial", 12), fg="#5A1E76", bg="#5A1E76", activebackground="#5A1E76", activeforeground="#5A1E76", borderwidth=0, highlightthickness = 0, bd = 0, cursor="hand1")
ab_button.config(image=images["alpha_beta"])
ab_button.place(x=977, y=230, width=221, height=111)
########################
h1i = PhotoImage(file="h.png")
h1_button = tk.Button(root, text="", command=lambda: set_ai_strategy("heuristic_minimax_1"), font=("Arial", 12), fg="#5A1E76", bg="#5A1E76", activebackground="#5A1E76", activeforeground="#5A1E76", borderwidth=0, highlightthickness = 0, bd = 0, cursor="hand1")
h1_button.config(image=images["heuristic_1"])
h1_button.place(x=977, y=375, width=221, height=111)
########################
h2i = PhotoImage(file="h2.png")
h2_button = tk.Button(root, text="", command=lambda: set_ai_strategy("heuristic_minimax_2"), font=("Arial", 12), fg="#5A1E76", bg="#5A1E76", activebackground="#5A1E76", activeforeground="#5A1E76", borderwidth=0, highlightthickness = 0, bd = 0, cursor="hand1")
h2_button.config(image=images["heuristic_2"])
h2_button.place(x=977, y=523, width=221, height=111)
########################
# Right Panel for Tic-Tac-Toe grid
right_panel = tk.Frame(canvas, width=800, height=800, bg='#2B0040')
right_panel.place(x=440, y=150)

buttons = []
def createbuttons():
    global buttons
    for i in range(9):
        button = tk.Button(right_panel, text="", width=100, height=100, fg="#2B0040", bg="#2B0040", activebackground="#2B0040", activeforeground="#2B0040", borderwidth=0, highlightthickness=0, bd=0, cursor="hand1", command=lambda i=i: on_button_click(i))
        button.config(image=images["play"])
        button.grid(row=i // 3, column=i % 3, padx=16, pady=16)
        buttons.append(button)

status_label = Label(canvas, text="Select your move.", image=images["amove"], font=("Arial", 14), foreground='#2B0040', background='#2B0040')
status_label.place(x=527, y=58)

button=[]
createbuttons()

# Exit button at the top right
exit_button = tk.Button(root, text="", command=root.quit, font=("Arial", 12), fg="#5A1E76", bg="#5A1E76", activebackground="#5A1E76", activeforeground="#5A1E76", borderwidth=0, highlightthickness = 0, bd = 0, cursor="hand1")
exit_button.config(image=images["exit"])
exit_button.place(x=13, y=11, width=80, height=80)

# Reset button
exit_button = tk.Button(root, text="", command=lambda: reset_game(), font=("Arial", 12), fg="#2B0040", bg="#2B0040", activebackground="#2B0040", activeforeground="#2B0040", borderwidth=0, highlightthickness = 0, bd = 0, cursor="hand1")
exit_button.config(image=images["reset"])
exit_button.place(x=527, y=578, width=227, height=107)

reset_game()

root.mainloop()
