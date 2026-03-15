import pygame

# --- CONFIG ---
WIDTH = 600
ROWS = 30
CELL_SIZE = WIDTH // ROWS
SIDE_MARGIN = 260  

# Colors
WHITE, BLACK, DARK_GREY = (255, 255, 255), (0, 0, 0), (50, 50, 50)
GREEN, RED, BLUE = (0, 255, 0), (255, 0, 0), (0, 0, 255)
PURPLE, YELLOW, ORANGE = (128, 0, 128), (255, 255, 0), (255, 165, 0)
CYAN, MAGENTA, BG_COLOR = (0, 255, 255), (255, 0, 255), (30, 30, 30)

pygame.init()
FONT = pygame.font.SysFont("Arial", 14)
