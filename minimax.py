import math
import tkinter as tk

X = "X"
O = "O"
EMPTY = None
count = 0

def evaluate(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != EMPTY:
            return 1 if board[row][0] == X else -1
        if board[0][row] == board[1][row] == board[2][row] != EMPTY:
            return 1 if board[0][row] == X else -1
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return 1 if board[0][0] == X else -1
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return 1 if board[0][2] == X else -1
    return 0  # Beraberlik

def minimax(board, depth, alpha, beta, is_maximizing):
    score = evaluate(board)
    if score != 0:
        return score

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = X
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  # Beta cut-off
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = O
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # Alpha cut-off
        return best_score

def find_best_move(board):
    best_score = -math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = X
                score = minimax(board, 0, alpha, beta, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def handle_click(row, col):
    global current_player, board, buttons, count

    if board[row][col] == EMPTY:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player)
        count += 1

        winner = evaluate(board)
        if winner == 1:
            info_label.config(text="AI wins!")
            disable_buttons()
        elif winner == -1:
            info_label.config(text="You win!")
            disable_buttons()
        elif winner == 0 and count == 9:
            info_label.config(text="It's a draw!")
            disable_buttons()

        current_player = O if current_player == X else X

        if current_player == X and winner == 0:
            ai_move = find_best_move(board)
            handle_click(ai_move[0], ai_move[1])


def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Tic Tac Toe")

board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(window, text="", font=('Arial', 20), width=4, height=2,
                           command=lambda row=i, col=j: handle_click(row, col))
        button.grid(row=i, column=j, padx=5, pady=5)
        row_buttons.append(button)
    buttons.append(row_buttons)

ai_move = find_best_move(board)
board[ai_move[0]][ai_move[1]] = X
buttons[ai_move[0]][ai_move[1]].config(text=X)
count += 1

info_label = tk.Label(window, text="Your move (O)", font=('Arial', 14))
info_label.grid(row=3, columnspan=3)

current_player = O  

window.mainloop()
