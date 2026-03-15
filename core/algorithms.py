import random
from queue import PriorityQueue
from core.heuristics import h
from config import ROWS, GREEN, RED, PURPLE, ORANGE, CYAN, MAGENTA

def reconstruct_path(came_from, current, draw):
    length = 0
    while current in came_from:
        current = came_from[current]
        if not current.is_start() and not current.is_end():
            current.make_path()
            length += 1
        draw()
    return length

def bfs(draw, grid, start, end):
    queue, visited, came_from = [start], {start}, {}
    nodes_exp = 0
    while queue:
        current = queue.pop(0)
        nodes_exp += 1
        if current == end: return nodes_exp, reconstruct_path(came_from, end, draw)
        for n in current.neighbors:
            if n not in visited:
                visited.add(n)
                came_from[n] = current
                if n != end: n.make_open(GREEN)
                queue.append(n)
        draw()
        if current != start: current.make_closed(RED)
    return nodes_exp, 0

def dfs(draw, grid, start, end):
    stack, visited, came_from = [start], {start}, {}
    nodes_exp = 0
    while stack:
        current = stack.pop()
        nodes_exp += 1
        if current == end: return nodes_exp, reconstruct_path(came_from, end, draw)
        for n in current.neighbors:
            if n not in visited:
                visited.add(n)
                came_from[n] = current
                if n != end: n.make_open(PURPLE)
                stack.append(n)
        draw()
        if current != start: current.make_closed(ORANGE)
    return nodes_exp, 0

def astar(draw, grid, start, end, weight=1):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from, g_score = {}, {n: float("inf") for r in grid for n in r}
    g_score[start], nodes_exp = 0, 0
    while not open_set.empty():
        current = open_set.get()[2]
        nodes_exp += 1
        if current == end: return nodes_exp, reconstruct_path(came_from, end, draw)
        for n in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[n]:
                came_from[n] = current
                g_score[n] = temp_g
                count += 1
                open_set.put((temp_g + weight * h(n.get_pos(), end.get_pos()), count, n))
                if n != end: n.make_open(CYAN)
        draw()
        if current != start: current.make_closed(MAGENTA)
    return nodes_exp, 0

def bidirectional_astar(draw, grid, start, end):
    count = 0
    f_open, b_open = PriorityQueue(), PriorityQueue()
    f_open.put((0, count, start))
    b_open.put((0, count, end))
    f_came, b_came = {}, {}
    f_g, b_g = {n: float("inf") for r in grid for n in r}, {n: float("inf") for r in grid for n in r}
    f_g[start], b_g[end] = 0, 0
    nodes_exp = 0
    while not f_open.empty() and not b_open.empty():
        cf = f_open.get()[2]
        nodes_exp += 1
        if cf in b_came: return nodes_exp, reconstruct_path(f_came, cf, draw) + reconstruct_path(b_came, cf, draw)
        for n in cf.neighbors:
            if f_g[cf] + 1 < f_g[n]:
                f_came[n], f_g[n] = cf, f_g[cf] + 1
                f_open.put((f_g[n] + h(n.get_pos(), end.get_pos()), count, n))
                if not n.is_start() and not n.is_end(): n.make_open(RED)
        cb = b_open.get()[2]
        nodes_exp += 1
        if cb in f_came: return nodes_exp, reconstruct_path(f_came, cb, draw) + reconstruct_path(b_came, cb, draw)
        for n in cb.neighbors:
            if b_g[cb] + 1 < b_g[n]:
                b_came[n], b_g[n] = cb, b_g[cb] + 1
                b_open.put((b_g[n] + h(n.get_pos(), start.get_pos()), count, n))
                if not n.is_start() and not n.is_end(): n.make_open(ORANGE)
        draw()
    return nodes_exp, 0

def jump(r, c, dr, dc, end, grid):
    nr, nc = r + dr, c + dc
    if not (0 <= nr < ROWS and 0 <= nc < ROWS) or grid[nr][nc].is_barrier(): return None
    curr = grid[nr][nc]
    if curr == end: return curr
    if dr != 0:
        if (nc-1 >= 0 and grid[nr][nc-1].is_barrier() and not grid[nr+dr][nc-1].is_barrier()) or \
           (nc+1 < ROWS and grid[nr][nc+1].is_barrier() and not grid[nr+dr][nc+1].is_barrier()): return curr
    else:
        if (nr-1 >= 0 and grid[nr-1][nc].is_barrier() and not grid[nr-1][nc+dc].is_barrier()) or \
           (nr+1 < ROWS and grid[nr+1][nc].is_barrier() and not grid[nr+1][nc+dc].is_barrier()): return curr
    return jump(nr, nc, dr, dc, end, grid)

def jps(draw, grid, start, end):
    count, open_set = 0, PriorityQueue()
    open_set.put((0, count, start))
    came_from, g_score = {}, {n: float("inf") for r in grid for n in r}
    g_score[start], nodes_exp = 0, 0
    while not open_set.empty():
        current = open_set.get()[2]
        nodes_exp += 1
        if current == end: return nodes_exp, reconstruct_path(came_from, end, draw)
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            jp = jump(current.row, current.col, dr, dc, end, grid)
            if jp:
                new_g = g_score[current] + h(current.get_pos(), jp.get_pos())
                if new_g < g_score[jp]:
                    came_from[jp], g_score[jp] = current, new_g
                    count += 1
                    open_set.put((new_g + h(jp.get_pos(), end.get_pos()), count, jp))
                    if not jp.is_start() and not jp.is_end(): jp.make_open(CYAN)
        draw()
        if current != start: current.make_closed(MAGENTA)
    return nodes_exp, 0

def recursive_maze(grid, r1, r2, c1, c2):
    if (r2 - r1) < 2 or (c2 - c1) < 2: return
    horiz = (r2 - r1) > (c2 - c1)
    if horiz:
        wall_r = random.randrange(r1 + 1, r2, 2)
        gap_c = random.randrange(c1, c2 + 1, 2)
        for c in range(c1, c2 + 1):
            if c != gap_c and not grid[wall_r][c].is_start() and not grid[wall_r][c].is_end(): grid[wall_r][c].make_barrier()
        recursive_maze(grid, r1, wall_r - 1, c1, c2)
        recursive_maze(grid, wall_r + 1, r2, c1, c2)
    else:
        wall_c = random.randrange(c1 + 1, c2, 2)
        gap_r = random.randrange(r1, r2 + 1, 2)
        for r in range(r1, r2 + 1):
            if r != gap_r and not grid[r][wall_c].is_start() and not grid[r][wall_c].is_end(): 
                grid[r][wall_c].make_barrier()
        recursive_maze(grid, r1, r2, c1, wall_c - 1)
        recursive_maze(grid, r1, r2, wall_c + 1, c2)
