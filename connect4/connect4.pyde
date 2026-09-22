column = 7
row = 6
size = 80
off_x = 50
off_y = 50

board = []
current_player = 1
gameover = False
winner = 0

def setup():
    size(700, 600)
    init_board()

def init_board():
    global board, current_player, gameover, winner
    board = create_2d_array(column, row)
    current_player = 1
    gameover = False
    winner = 0

def create_2d_array(cols, rows):
    if rows <= 0:
        return []
    return [create_1d_array(cols)] + create_2d_array(cols, rows - 1)

def create_1d_array(length):
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
    
    x = off_x + c_idx * size
    y = off_y + r_idx * size
    
    noFill()
    stroke(0)
    strokeWeight(1)
    rect(x, y, size, size)
    
    val = board[r_idx][c_idx]
    if val != 0:
        if val == 1:
            fill(0)
        else:
            fill(255)
        stroke(0)
        ellipse(x + size / 2, y + size / 2, size - 12, size - 12)
        
    draw_grid_2d(c - 1, r)
