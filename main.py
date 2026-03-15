import pygame
import sys
import time
import random
from config import WIDTH, SIDE_MARGIN, BG_COLOR, ROWS, CELL_SIZE, WHITE, BLACK, GREEN, PURPLE, CYAN, MAGENTA, ORANGE, BLUE, FONT
from core.engine import Node
from ui.components import Button
from core.algorithms import bfs, dfs, astar, bidirectional_astar, jps, recursive_maze

def setup_maze(grid):
    for r in grid: 
        for n in r: n.reset()
    s, e = grid[0][0], grid[ROWS-1][ROWS-1]
    s.make_start(); e.make_end()
    return s, e

def main():
    WIN = pygame.display.set_mode((WIDTH + SIDE_MARGIN, WIDTH))
    pygame.display.set_caption("PathQuest Lab")
    grid = [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]
    start, end = setup_maze(grid)
    metrics = None
    
    btns = [
        Button(WIDTH+10, 10, 115, 30, "BFS", GREEN), Button(WIDTH+135, 10, 115, 30, "DFS", PURPLE),
        Button(WIDTH+10, 45, 115, 30, "A*", CYAN), Button(WIDTH+135, 45, 115, 30, "Dijkstra", MAGENTA),
        Button(WIDTH+10, 80, 115, 30, "Bidirectional", ORANGE), Button(WIDTH+135, 80, 115, 30, "JPS", BLUE),
        Button(WIDTH+10, 125, 240, 30, "Maze: Structured", (50,80,120)),
        Button(WIDTH+10, 160, 240, 30, "Maze: Random", (60,100,60)),
        Button(WIDTH+10, 195, 240, 30, "Reset Path Only", (100,100,150)),
        Button(WIDTH+10, 230, 240, 30, "Clear All", (150,50,50))
    ]

    while True:
        WIN.fill(BG_COLOR)
        for r in grid: 
            for n in r: n.draw(WIN)
        for b in btns: b.draw(WIN)
        
        if metrics:
            pygame.draw.rect(WIN, WHITE, (WIDTH+10, 306, 240, 85))
            txts = [f"Algo: {metrics[0]}", f"Nodes: {metrics[1]}", f"Path: {metrics[2]}", f"Time: {metrics[3]:.2f}ms"]
            for i, t in enumerate(txts): WIN.blit(FONT.render(t, True, BLACK), (WIDTH+20, 312 + i*18))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] < WIDTH:
                    r, c = pos[0]//CELL_SIZE, pos[1]//CELL_SIZE
                    node = grid[r][c]
                    if not start and node != end: start = node; node.make_start()
                    elif not end and node != start: end = node; node.make_end()
                    elif node != start and node != end: node.make_barrier()
                else:
                    for b in btns:
                        if b.is_clicked(pos):
                            if b.text == "Clear All": 
                                grid = [[Node(i,j) for j in range(ROWS)] for i in range(ROWS)]
                                start, end, metrics = None, None, None
                            elif b.text == "Reset Path Only": 
                                for r in grid: 
                                    for n in r: n.reset_path()
                                metrics = None
                            elif b.text == "Maze: Random":
                                start, end = setup_maze(grid)
                                for r in grid: 
                                    for n in r:
                                        if not n.is_start() and not n.is_end() and random.random() < 0.3: n.make_barrier()
                            elif b.text == "Maze: Structured":
                                start, end = setup_maze(grid)
                                recursive_maze(grid, 0, ROWS-1, 0, ROWS-1)
                            elif start and end:
                                for r in grid: 
                                    for n in r: n.reset_path(); n.update_neighbors(grid)
                                end.make_end() 
                                def d():
                                    for row in grid: 
                                        for n in row: n.draw(WIN)
                                    pygame.display.update()
                                t0 = time.perf_counter()
                                if b.text == "BFS": res = bfs(d, grid, start, end)
                                elif b.text == "DFS": res = dfs(d, grid, start, end)
                                elif b.text == "A*": res = astar(d, grid, start, end)
                                elif b.text == "Dijkstra": res = astar(d, grid, start, end, weight=0)
                                elif b.text == "Bidirectional": res = bidirectional_astar(d, grid, start, end)
                                elif b.text == "JPS": res = jps(d, grid, start, end)
                                metrics = (b.text, res[0], res[1], (time.perf_counter()-t0)*1000)
        pygame.display.update()

if __name__ == "__main__":
    main()
