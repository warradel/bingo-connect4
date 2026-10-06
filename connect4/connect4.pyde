import os

column = 7
row = 6
c_size = 80
off_x = 50
off_y = 50

board = []
current_player = 1
gameover = False
winner = 0

score_p1 = 0
score_p2 = 0

def setup():
    size(700, 650)
    init_board()

def init_board():
    global board, current_player, gameover, winner
    board = create_2d_array(column, row)
    current_player = 1
    gameover = False
    winner = 0

def create_2d_array(cols, rows): #vertical
    if rows <= 0:
        return []
    return [create_1d_array(cols)] + create_2d_array(cols, rows - 1)

def create_1d_array(length): #horizontal
    if length <= 0:
        return []
    return [0] + create_1d_array(length - 1)

def draw():
    background(255)
    draw_grid_2d(column, row)
    draw_ui()

def draw_grid_2d(c, r):
    if r <= 0:
        return
    if c <= 0:
        draw_grid_2d(column, r - 1)
        return
    
    r_idx = row - r
    c_idx = column - c
    
    x = off_x + c_idx * c_size
    y = off_y + r_idx * c_size
    
    stroke(0)
    strokeWeight(1)
    line(x, y, x + c_size, y)                 # Top
    line(x + c_size, y, x + c_size, y + c_size) # Right
    line(x + c_size, y + c_size, x, y + c_size) # Bottom
    line(x, y + c_size, x, y)                 # Left
    
    val = board[r_idx][c_idx]
    if val != 0:
        if val == 1:
            fill(0)
        else:
            fill(255)
        stroke(0)
        ellipse(x + c_size / 2, y + c_size / 2, c_size - 12, c_size - 12)
        
    draw_grid_2d(c - 1, r)

def draw_ui():
    fill(0)
    textSize(18)
    textAlign(LEFT, TOP)
    
    score_text = "SCORE => P1 (BLACK): " + str(score_p1) + " | P2 (WHITE): " + str(score_p2)
    text(score_text, off_x, 15)
    
    ui_y = off_y + row * c_size + 20
    
    if not gameover:
        msg = "TURN: PLAYER " + str(current_player) + " (" + ("BLACK" if current_player == 1 else "WHITE") + ")"
        text(msg, off_x, ui_y)
    else:
        if winner == 0:
            text("GAME OVER: DRAW! (CLICK TO RESTART)", off_x, ui_y)
        else:
            text("GAME OVER: PLAYER " + str(winner) + " WINS! (CLICK TO RESTART)", off_x, ui_y)

def mousePressed():
    if gameover:
        init_board()
        return
    
    if mouseX >= off_x and mouseX < off_x + column * c_size:
        if mouseY >= off_y and mouseY < off_y + row * c_size:
            col = int((mouseX - off_x) / c_size)
            drop_disc(col)


def drop_disc(col):
    global current_player
    r = find_lowest_row(col, row - 1)
    if r != -1:
        board[r][col] = current_player
        check_game_over()
        if not gameover:
            current_player = 3 - current_player
        return True
    return False

def find_lowest_row(col, r):
    if r < 0:
        return -1
    if board[r][col] == 0:
        return r
    return find_lowest_row(col, r - 1)

def check_game_over():
    global gameover, winner, score_p1, score_p2
    if scan_win(0, 0):
        gameover = True
        winner = current_player
        
        if winner == 1:
            score_p1 += 1
        elif winner == 2:
            score_p2 += 1

    elif check_full_board(0):
        gameover = True
        winner = 0

def scan_win(c, r):
    if r >= row:
        return False
    if c >= column:
        return scan_win(0, r + 1)
        
    if board[r][c] == current_player:
        if check_board_win(c, r):
            return True
            
    return scan_win(c + 1, r)

def check_full_board(c):
    if c >= column:
        return True
    if board[0][c] == 0:
        return False
    return check_full_board(c + 1)

def check_board_win(c, r):
    p = board[r][c]
    
    if (1 + count_line(c + 1, r, 1, 0, p) + count_line(c - 1, r, -1, 0, p)) >= 4:
        return True
    if (1 + count_line(c, r + 1, 0, 1, p)) >= 4:
        return True
    if (1 + count_line(c + 1, r + 1, 1, 1, p) + count_line(c - 1, r - 1, -1, -1, p)) >= 4:
        return True
    if (1 + count_line(c + 1, r - 1, 1, -1, p) + count_line(c - 1, r + 1, -1, 1, p)) >= 4:
        return True
        
    return False

def count_line(c, r, dc, dr, player):
    if c < 0 or c >= column or r < 0 or r >= row:
        return 0
    if board[r][c] != player:
        return 0
    return 1 + count_line(c + dc, r + dr, dc, dr, player)

def save_game():
    global board, current_player, gameover, score_p1, score_p2
    if gameover:
        print("[SYSTEM]: Cannot save a finished game.")
        return

    board_string = ""
    r = 0
    while r < row:
        c = 0
        while c < column:
            board_string += str(board[r][c])
            c += 1
        r += 1
            
    save_data = board_string + "|" + str(current_player) + "|" + str(score_p1) + "|" + str(score_p2)
    save_path = sketchPath("c4_save.txt")
    
    with open(save_path, "w") as f:
        f.write(save_data)
    print("[SYSTEM]: Game saved successfully at:", save_path)

def load_game():
    global board, current_player, gameover, winner, score_p1, score_p2
    
    save_path = sketchPath("c4_save.txt")
    
    if not os.path.exists(save_path):
        print("[SYSTEM]: Save file not found at:", save_path)
        return
        
    try:
        with open(save_path, "r") as f:
            save_data = f.read()
            
        parts = save_data.split("|")
        board_part = parts[0]
        current_player = int(parts[1])
    
        if len(parts) >= 4:
            score_p1 = int(parts[2])
            score_p2 = int(parts[3])
            
        gameover = False
        winner = 0
        
        new_board = []
        idx = 0
        r = 0
        while r < row:
            row_data = []
            c = 0
            while c < column:
                row_data.append(int(board_part[idx]))
                idx += 1
                c += 1
            new_board.append(row_data)
            r += 1
            
        board = new_board
        print("[SYSTEM]: Game loaded successfully!")
        
    except Exception as e:
        print("[ERROR]: Corrupted save file:", e)

def keyPressed():
    if key == 's' or key == 'S':
        save_game()
    elif key == 'l' or key == 'L':
        load_game()
