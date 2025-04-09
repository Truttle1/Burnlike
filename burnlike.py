from copy import deepcopy
import pygame
import sys
import pickle

auto = False

# CONSTANTS, FEEL FREE TO CHANGE
BLOCK_SIZE = 4
WIDTH = 12
HEIGHT = 11
HIGHLIGHT = True
GOOD_BOARDS_FILE = "good_boards.pickle"
#####



CENTER = True

class Cell:
    def __init__(self, r, g, b):
        self.channels = [r, g, b]
        self.max_channels = [r, g, b]
        self.min_channels = [r, g, b]

    def __repr__(self):
        return f"{self.channels[0]}{self.channels[1]}{self.channels[2]}"
    
    def maximum_str(self):
        return f"{self.max_channels[0]}{self.max_channels[1]}{self.max_channels[2]}"

    def minimum_str(self):
        return f"{self.min_channels[0]}{self.min_channels[1]}{self.min_channels[2]}"

    def set_bounds(self, neighbors):
        for i in range(3):
            for neighbor in neighbors:
                self.max_channels[i] = max(self.max_channels[i], neighbor.channels[i])
                self.min_channels[i] = min(self.min_channels[i], neighbor.channels[i])
    
    def deepcopy(self):
        return Cell(self.channels[0], self.channels[1], self.channels[2])
    
    

def get_cell_neighbors(board, r, c, diagonal=False):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not diagonal and i != 0 and j != 0:
                continue
            if i == 0 and j == 0:
                continue
            if r + i < 0 and c + j >= 0 and c + j < len(board[0]):
                neighbors.append(ORIGINAL_BOARD[-1][c + j])
                continue
            if r + i >= len(board) and c + j >= 0 and c + j < len(board[0]):
                neighbors.append(ORIGINAL_BOARD[0][c + j])
                continue
            if c + j < 0 and r + i >= 0 and r + i < len(board):
                neighbors.append(ORIGINAL_BOARD[r + i][-1])
                continue
            if r + i >= 0 and r + i < len(board) and c + j >= len(board[r + i]):
                neighbors.append(ORIGINAL_BOARD[r + i][0])
                continue
            if c + j < len(board[0]) and r + i >= 0 and r + i < len(board) and c + j >= 0:
                neighbors.append(board[r + i][c + j])
    return neighbors

def update_cell(prev_board, old_board, new_board, i, j):
    neighbors = get_cell_neighbors(old_board, i, j)
    new_board[i][j].set_bounds(neighbors)
    #difference = get_difference_of_cell(old_board, i, j, center=CENTER)
    difference_change = get_difference_change_of_cell(prev_board, old_board, i, j)
    # print(f"AT [{j}, {i}] STARTING: {new_board[i][j].channels} DIFFERENCE: {difference}")
    override = 0


    for channel in range(1, 3):
        # Flood fill?
        if difference_change[channel] == 1:
            new_board[i][j].channels[channel] = max(old_board[i][j].channels[channel] - 1, new_board[i][j].min_channels[channel])
        
        
        
        if difference_change[channel] == 2:
            for c in range(3):
                new_board[i][j].channels[c] = max(old_board[i][j].channels[c] - 2, new_board[i][j].min_channels[c])
        
    # This feels like it's too pigeonholed
    # Maybe there's a better rule, but this is causing rule110 to materialize...

    if i > 0:
        has_3 = False
        for channel in range(3):
            if new_board[i - 1][j].channels[channel] >= 3:
                has_3 = True
        if has_3:
            new_board[i][j].channels[0] = old_board[i][j].channels[0]
            new_board[i][j].channels[1] = old_board[i][j].channels[1]
            new_board[i][j].channels[2] = old_board[i][j].channels[2]

            


    # print(f"AT [{j}, {i}] NOW: {new_board[i][j].channels}")
    
    if old_board[i][j]:
        pass
    return new_board

def get_difference_of_cell(board, i, j, diagonal=False, center=False):
    result = [0, 0, 0]
    neighbors = get_cell_neighbors(board, i, j, diagonal)
    for channel in range(3):
        neighbor_sum = 0
        for neighbor in neighbors:
            neighbor_sum += neighbor.channels[channel]
        difference = abs(board[i][j].channels[channel] - neighbor_sum)
        if not center:
            difference = abs(neighbor_sum)
        result[channel] = difference
    return result
        

def get_difference_change_of_cell(board, old_board, i, j, diagonal=False):
    diff_old = get_difference_of_cell(old_board, i, j, diagonal, CENTER)
    diff_new = get_difference_of_cell(board, i, j, diagonal, CENTER)

    return [abs(diff_new[i] - diff_old[i]) for i in range(3)]

board = []

def update_board(prev_board, board):
    new_board = deepcopy(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            new_board = update_cell(prev_board, board, new_board, i, j)
    #print_board(new_board)
    return new_board


def print_board_max(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j].maximum_str(), end=" ")
        print()
    print('------------------')

def print_board_min(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j].minimum_str(), end=" ")
        print()
    print('------------------')

def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end=" ")
        print()
    print('------------------')


def tile_horizontal(board, n=2):
    new_board = []
    height = len(board)

    for i in range(height):
        new_board.append([])
        for _ in range(n):
            for j in range(len(board[i])):
                new_board[i].append(board[i][j].deepcopy())
    return new_board

def tile_vertical(board, n=2):
    new_board = []
    height = len(board)
    for z in range(n):
        for i in range(height):
            new_board.append([])
            for j in range(len(board[i])):
                new_board[height * z + i].append(board[i][j].deepcopy())
    return new_board

def copy_board(board):
    new_board = []
    for i in range(len(board)):
        new_board.append([])
        for j in range(len(board[i])):
            new_board[i].append(board[i][j].deepcopy())
    return new_board

#############

def filter(board, pattern, start_row, start_col):
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            for c in range(3):
                if board[start_row + i][start_col + j].channels[c] != pattern[i][j].channels[c]:
                    return False
    return True

def get_sub_board(board, start_row, start_col, height, width):
    sub_board = []
    for i in range(height):
        sub_board.append([])
        for j in range(width):
            sub_board[i].append(board[start_row + i][start_col + j].deepcopy())
    return sub_board

#############

with open(sys.argv[1], "r") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        board_line = []
        line = lines[i].strip()
        if line == "":
            continue
        for cell in line.split():
            if len(cell) == 2:
                board_line.append(Cell(0, int(cell[0]), int(cell[1])))
            elif len(cell) == 3:
                board_line.append(Cell(int(cell[0]), int(cell[1]), int(cell[2])))
        board.append(board_line)



ORIGINAL_WIDTH = len(board[0])
ORIGINAL_HEIGHT = len(board)


board = tile_horizontal(board, WIDTH)
board = tile_vertical(board, HEIGHT)

SCREEN_WIDTH = BLOCK_SIZE * len(board[0])
SCREEN_HEIGHT = BLOCK_SIZE * len(board)

print(SCREEN_WIDTH, SCREEN_HEIGHT)

prev_board = copy_board(board)

# PARAMETER: Cell(s) to disrupt at the start
board[0][2+(6*(WIDTH - 1))].channels = [0, 0, 0]
###

ORIGINAL_BOARD = deepcopy(board)

for i in range(len(ORIGINAL_BOARD)):
    for j in range(len(ORIGINAL_BOARD[i])):
        ORIGINAL_BOARD[i][j] = ORIGINAL_BOARD[i][j].deepcopy()


pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Consolas', 12)

view = 0
good_boards = []

try:
    with open(GOOD_BOARDS_FILE, "rb") as fp:
        good_boards = pickle.load(fp)
except:
    pass

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True
clock = pygame.time.Clock()
while running:
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (255, 0, 0), (mouse[0] - 4, mouse[1] - 4, 16, 16))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # To add good boards (highlighted yellow), remove the False and click on the cell. It stores in the pickle.
            if False and event.button == 1:
                x = event.pos[0] // (ORIGINAL_WIDTH * BLOCK_SIZE)
                y = event.pos[1] // (ORIGINAL_HEIGHT * BLOCK_SIZE)
                print(f"Clicked on cell ({x}, {y})")
                good_boards.append(get_sub_board(board, y * ORIGINAL_HEIGHT, x * ORIGINAL_WIDTH, ORIGINAL_HEIGHT, ORIGINAL_WIDTH))
                with open(GOOD_BOARDS_FILE, "wb") as fp: 
                    pickle.dump(good_boards, fp)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LALT:  
                view = (view + 1) % 4
            if event.key == pygame.K_LSHIFT:
                auto = not auto
            elif event.key == pygame.K_SPACE:
                tmp = copy_board(board)
                board = update_board(prev_board, board)
                prev_board = tmp                
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in range(len(board)):
        for j in range(len(board[i])):
            color = (min((board[i][j].channels[0] / 3.0) * 1.1 * 255, 255), 
                     min((board[i][j].channels[2] / 3.0) * 1.1 * 255, 255), 
                     min((board[i][j].channels[1] / 3.0) * 1.1 * 255, 255))
            pygame.draw.rect(screen, color, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            if BLOCK_SIZE == 16:
                txt_color = (255, 255, 255)
                if board[i][j].channels[2] >= 2:
                    txt_color = (0, 0, 0)
                if view == 2:
                    text = font.render(str(get_difference_of_cell(board, i, j, center=CENTER)[1]) + str(get_difference_of_cell(board, i, j, center=CENTER)[2]), True, txt_color)
                elif view == 1:
                    text = font.render(str(get_difference_change_of_cell(prev_board, board, i, j)[1]) + str(get_difference_change_of_cell(prev_board, board, i, j)[2]), True, txt_color)
                elif view == 0:
                    text = font.render(str(board[i][j].channels[1]) + str(board[i][j].channels[2]), True, txt_color)
                else:
                    text = font.render('', True, txt_color)
            
            
                screen.blit(text, (j * BLOCK_SIZE, i * BLOCK_SIZE))
    for row in range(HEIGHT):
        for col in range(WIDTH):
            pygame.draw.rect(screen, (255, 255, 255), (col * BLOCK_SIZE * ORIGINAL_WIDTH, row * BLOCK_SIZE * ORIGINAL_HEIGHT, ORIGINAL_WIDTH * BLOCK_SIZE, ORIGINAL_HEIGHT * BLOCK_SIZE), 1)
            for brd in good_boards:
                if HIGHLIGHT and filter(board, brd, row * ORIGINAL_HEIGHT, col * ORIGINAL_WIDTH):
                    pygame.draw.rect(screen, (255, 255, 0), (col * BLOCK_SIZE * ORIGINAL_WIDTH, row * BLOCK_SIZE * ORIGINAL_HEIGHT, ORIGINAL_WIDTH * BLOCK_SIZE, ORIGINAL_HEIGHT * BLOCK_SIZE), 0)
    clock.tick(5)
    pygame.display.flip()
    if auto:
        tmp = copy_board(board)
        board = update_board(prev_board, board)
        prev_board = tmp       