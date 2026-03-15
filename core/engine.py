import pygame
from config import WHITE, BLACK, DARK_GREY, BLUE, PURPLE, CELL_SIZE, ROWS

class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.x, self.y = row * CELL_SIZE, col * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf")
        self.rhs = float("inf")

    def get_pos(self): return self.row, self.col
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == BLUE
    def is_end(self): return self.color == PURPLE
    def reset(self): self.color = WHITE
    def reset_path(self):
        if self.color not in [BLUE, PURPLE, BLACK]: self.color = WHITE
    def make_start(self): self.color = BLUE
    def make_end(self): self.color = PURPLE
    def make_barrier(self): self.color = BLACK
    def make_path(self, color=(255, 255, 0)): self.color = color
    def make_open(self, color): self.color = color
    def make_closed(self, color): self.color = color
    def __lt__(self, other): return False 

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(win, DARK_GREY, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)

    def update_neighbors(self, grid):
        self.neighbors = []
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < ROWS and not grid[r][c].is_barrier():
                self.neighbors.append(grid[r][c])
