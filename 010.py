# Bug Fix
import pygame
import sys
import random
import threading
import time
from collections import deque

BG = (30, 30, 30)
WLL = (120, 120, 120)
PLYR = (255, 255, 0)
R_GHST = (255, 0, 0)
P_GHST = (255, 192, 203)
B_GHST = (0, 0, 255)

board_y = 29
board_x = 28

length = 10
step = max(1, length // 10)
gap = 4
speed = 1.0 / 100               

scrn_y = board_y * length
scrn_x = board_x * length
tab_y = board_y * (length + gap) + gap
tab_x = board_x * (length + gap) + gap

plyr = [0, 0]
scrn = []
old_drct = 0
drct = 0  
ghost = [] 
ghst_drct = []
game_over = False

ghst_start = 0
difference = 3

for y in range(scrn_y): 
    scrn.append([0] * scrn_x)
for id in range(4): 
    ghst_drct.append([0] * 5)
    ghost.append([0] * 2)

board = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
lock_plyr = threading.Lock()
lock_red = threading.Lock()
lock_pink = threading.Lock()
lock_blue = threading.Lock()

def check(direction, cord):
    r_idx = cord[0] // length
    
    if r_idx == 12:
        if direction == 9 and cord[1] <= 0: return True
        if direction == 3 and cord[1] >= (board_x - 1) * length: return True

    if direction == 3: return (cord[1] + 1 < scrn_x) and all(scrn[cord[0] + y][cord[1] + x + step] != 1 for y in range(length) for x in range(length))
    elif direction == 6: return (cord[0] + 1 < scrn_y) and all(scrn[cord[0] + y + step][cord[1] + x] != 1 for y in range(length) for x in range(length))
    elif direction == 9: return (cord[1] - 1 >= 0) and all(scrn[cord[0] + y][cord[1] + x - step] != 1 for y in range(length) for x in range(length))
    elif direction == 12: return (cord[0] - 1 >= 0) and all(scrn[cord[0] + y - step][cord[1] + x] != 1 for y in range(length) for x in range(length))
    return False

def opposite_dir(d):
    if d == 3: return 9
    if d == 9: return 3
    if d == 6: return 12
    if d == 12: return 6
    return 0

def shortest_path(start_tile, target_tile):
    sr, sc = start_tile
    tr, tc = target_tile
    tr = max(0, min(board_y - 1, tr))
    tc = max(0, min(board_x - 1, tc))
    
    if (sr, sc) == (tr, tc):
        return None
    
    queue = deque([(sr, sc)])
    visited = {(sr, sc)}
    parent = {}
    
    directions = [
        (3, 0, 1),
        (6, 1, 0),
        (9, 0, -1),
        (12, -1, 0)
    ]
    
    found = False
    while queue:
        r, c = queue.popleft()
        if (r, c) == (tr, tc):
            found = True
            break
            
        for d, dr, dc in directions:
            nr, nc = r + dr, c + dc
            if nr == 12 and (nc < 0 or nc >= board_x):
                nc = nc % board_x
            if 0 <= nr < board_y and 0 <= nc < board_x and board[nr][nc] != 1:
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c, d)
                    queue.append((nr, nc))
                    
    if not found:
        return None
        
    curr = (tr, tc)
    first_step_dir = None
    while curr in parent:
        p_r, p_c, d = parent[curr]
        if (p_r, p_c) == (sr, sc):
            first_step_dir = d
            break
        curr = (p_r, p_c)
        
    return first_step_dir

def spawn():
    global plyr, drct, scrn, ghost
    plyr = [15 * length, 13 * length]
    for i in range(4):
        ghost[i] = [12 * length, (12 + i) * length]
    for y in range(scrn_y):
        for x in range(scrn_x):
            scrn[y][x] = board[y//length][x//length]
    drct = 0
    
def to_scrn(cord, state):
    for y in range(length):
        for x in range(length):
            scrn[cord[0] + y][cord[1] + x] = state

def draw(screen):
    for y in range(scrn_y):
        for x in range(scrn_x):
            Y = y + gap * (y//length)
            X = x + gap * (x//length)

            if scrn[y][x] == 0: 
                pygame.draw.rect(screen, BG, [X, Y, step, step], border_radius = 0)
            if scrn[y][x] == 1: 
                pygame.draw.rect(screen, WLL, [X, Y, step, step], border_radius = 0)
            if scrn[y][x] == 2: 
                pygame.draw.rect(screen, PLYR, [X, Y, step, step], border_radius = 1)
            if scrn[y][x] == 3: 
                pygame.draw.rect(screen, R_GHST, [X, Y, step, step], border_radius = 1)
            if scrn[y][x] == 4: 
                pygame.draw.rect(screen, P_GHST, [X, Y, step, step], border_radius = 1)
            if scrn[y][x] == 5: 
                pygame.draw.rect(screen, B_GHST, [X, Y, step, step], border_radius = 1)

def closest():
    global old_drct, drct
    if old_drct in (6, 12) and drct in (3, 9): 
        if plyr[0] % length <= gap or plyr[0] % length >= length - gap:
            plyr[0] = int(round(plyr[0], -1))
    if old_drct in (3, 9) and drct in (6, 12): 
        if plyr[1] % length <= gap or plyr[1] % length >= length - gap:
            plyr[1] = int(round(plyr[1], -1))

def move():
    global plyr, drct, game_over
    while not game_over:
        time.sleep(speed)
        with lock_plyr, lock_red, lock_pink:
            if game_over: break
            
            old_plyr = list(plyr)
            
            if drct == 3 and plyr[0] == 12 * length and plyr[1] >= (board_x - 1) * length: 
                plyr[1] = 0
            elif drct == 9 and plyr[0] == 12 * length and plyr[1] <= 0: 
                plyr[1] = (board_x - 1) * length
            else: 
                closest()
                if check(drct, plyr):
                    if drct == 3: plyr[1] += step
                    elif drct == 6: plyr[0] += step
                    elif drct == 9: plyr[1] -= step
                    elif drct == 12: plyr[0] -= step
            
            to_scrn(old_plyr, 0)
            to_scrn(plyr, 2)

def red():
    global ghost, ghst_drct, game_over
    time.sleep(ghst_start)
    
    cnt = 40
    id = 0

    while not game_over:
        time.sleep(speed * 3)
        
        with lock_plyr, lock_red, lock_pink, lock_blue:
            if game_over: 
                break
            to_scrn(ghost[id], 0)
            if cnt > 0:
                if cnt > 30: 
                    ghost[id][0] -= step
                elif cnt > 20: 
                    ghost[id][1] += step
                else: 
                    ghost[id][0] -= step
                cnt -= 1
                to_scrn(ghost[id], 3)
                continue
            
            if abs(ghost[id][0] - plyr[0]) < length and abs(ghost[id][1] - plyr[1]) < length:
                game_over = True
                break

            curr_d = ghst_drct[id][0]
            is_aligned = (ghost[id][0] % length == 0) and (ghost[id][1] % length == 0)
            all_valid_dirs = [d for d in [3, 6, 9, 12] if check(d, ghost[id])]
            opp_d = opposite_dir(curr_d)
            other_paths = [d for d in all_valid_dirs if d != opp_d]
            is_intersection = is_aligned and (len(other_paths) >= 2)
            
            if curr_d == 0 or not check(curr_d, ghost[id]) or is_intersection:
                start_tile = (ghost[id][0] // length, ghost[id][1] // length)
                target_tile = (plyr[0] // length, plyr[1] // length)
                best_d = shortest_path(start_tile, target_tile)

                forward_dirs = [d for d in all_valid_dirs if d != opp_d]
                
                if best_d is None or not check(best_d, ghost[id]) or best_d == opp_d:
                    if curr_d in forward_dirs:
                        best_d = curr_d
                    elif forward_dirs:
                        best_d = forward_dirs[0]
                    elif all_valid_dirs:
                        best_d = all_valid_dirs[0]
                    else:
                        best_d = curr_d if curr_d != 0 else 3
                        
                curr_d = best_d
                ghst_drct[id][0] = curr_d
            
            if curr_d == 3 and ghost[id][0] == 12 * length and ghost[id][1] >= (board_x - 1) * length: 
                ghost[id][1] = 0
            elif curr_d == 9 and ghost[id][0] == 12 * length and ghost[id][1] <= 0: 
                ghost[id][1] = (board_x - 1) * length
            elif check(curr_d, ghost[id]):
                if curr_d == 3: ghost[id][1] += step
                elif curr_d == 6: ghost[id][0] += step
                elif curr_d == 9: ghost[id][1] -= step
                elif curr_d == 12: ghost[id][0] -= step
                
            to_scrn(ghost[0], 3)

def pink():
    global ghost, ghst_drct, game_over, drct
    time.sleep(ghst_start + difference)
    
    cnt = 30
    id = 1

    while not game_over:
        time.sleep(speed * 3)
        
        with lock_plyr, lock_red, lock_pink, lock_blue:
            if game_over: 
                break
            to_scrn(ghost[id], 0)
            if cnt > 0:
                ghost[id][0] -= step
                cnt -= 1
                to_scrn(ghost[id], 4)
                continue
            
            if abs(ghost[id][0] - plyr[0]) < length and abs(ghost[id][1] - plyr[1]) < length:
                game_over = True
                break

            curr_d = ghst_drct[id][0]
            is_aligned = (ghost[id][0] % length == 0) and (ghost[id][1] % length == 0)
            all_valid_dirs = [d for d in [3, 6, 9, 12] if check(d, ghost[id])]
            opp_d = opposite_dir(curr_d)
            other_paths = [d for d in all_valid_dirs if d != opp_d]
            is_intersection = is_aligned and (len(other_paths) >= 2)
            
            if curr_d == 0 or not check(curr_d, ghost[id]) or is_intersection:
                start_tile = [ghost[id][0] // length, ghost[id][1] // length]
                base_target = [plyr[0] // length, plyr[1] // length]

                best_d = None
                for ahead in [4, 3, 2, 1, 0]:
                    target_tile = list(base_target)
                    if drct == 3:
                        target_tile[1] += ahead
                    elif drct == 9:
                        target_tile[1] -= ahead
                    elif drct == 6:
                        target_tile[0] += ahead
                    elif drct == 12:
                        target_tile[0] -= ahead

                    tr, tc = target_tile
                    if 0 <= tr < board_y and 0 <= tc < board_x:
                        best_d = shortest_path(start_tile, target_tile)
                        if best_d is not None:
                            break

                if best_d is None:
                    best_d = shortest_path(start_tile, base_target)

                forward_dirs = [d for d in all_valid_dirs if d != opp_d]
                if best_d == opp_d and forward_dirs:
                    best_d = forward_dirs[0]

                if best_d is None or not check(best_d, ghost[id]):
                    if forward_dirs:
                        best_d = forward_dirs[0]
                    elif all_valid_dirs:
                        best_d = all_valid_dirs[0]
                    else:
                        best_d = curr_d if curr_d != 0 else 3
                        
                curr_d = best_d
                ghst_drct[id][0] = curr_d
            
            if curr_d == 3 and ghost[id][0] == 12 * length and ghost[id][1] >= (board_x - 1) * length: 
                ghost[id][1] = 0
            elif curr_d == 9 and ghost[id][0] == 12 * length and ghost[id][1] <= 0: 
                ghost[id][1] = (board_x - 1) * length
            elif check(curr_d, ghost[id]):
                if curr_d == 3: ghost[id][1] += step
                elif curr_d == 6: ghost[id][0] += step
                elif curr_d == 9: ghost[id][1] -= step
                elif curr_d == 12: ghost[id][0] -= step
                
            to_scrn(ghost[id], 4)

def blue():
    global ghost, ghst_drct, game_over, drct
    time.sleep(ghst_start + difference * 3)
    
    cnt = 30
    id = 2
    ahead = 2
    target_tile = [0, 0]

    while not game_over:
        time.sleep(speed * 2)
        
        with lock_plyr, lock_red, lock_pink, lock_blue:
            if game_over: 
                break
            to_scrn(ghost[id], 0)
            if cnt > 0:
                ghost[id][0] -= step
                cnt -= 1
                to_scrn(ghost[id], 5)
                continue
            
            if abs(ghost[id][0] - plyr[0]) < length and abs(ghost[id][1] - plyr[1]) < length:
                game_over = True
                break

            curr_d = ghst_drct[id][0]
            is_aligned = (ghost[id][0] % length == 0) and (ghost[id][1] % length == 0)
            all_valid_dirs = [d for d in [3, 6, 9, 12] if check(d, ghost[id])]
            opp_d = opposite_dir(curr_d)
            other_paths = [d for d in all_valid_dirs if d != opp_d]
            is_intersection = is_aligned and (len(other_paths) >= 2)
            
            if curr_d == 0 or not check(curr_d, ghost[id]) or is_intersection:
                start_tile = [ghost[id][0] // length, ghost[id][1] // length]
                intermediate_tile = [plyr[0] // length, plyr[1] // length]

                if drct == 3:
                    intermediate_tile[1] += ahead
                elif drct == 9:
                    intermediate_tile[1] -= ahead
                elif drct == 6:
                    intermediate_tile[0] += ahead
                elif drct == 12:
                    intermediate_tile[0] -= ahead
                
                red_tile = [ghost[0][0] // length, ghost[0][1] // length]
                target_tile = [
                    intermediate_tile[0] + (intermediate_tile[0] - red_tile[0]),
                    intermediate_tile[1] + (intermediate_tile[1] - red_tile[1])
                ]

                forward_dirs = [d for d in all_valid_dirs if d != opp_d]
                candidate_dirs = forward_dirs if forward_dirs else all_valid_dirs
                
                best_d = None
                min_dist = float('inf')
                
                dir_offsets = {
                    3: (0, 1),
                    6: (1, 0),
                    9: (0, -1),
                    12: (-1, 0)
                }
                
                for d in candidate_dirs:
                    dr, dc = dir_offsets[d]
                    next_tile = (start_tile[0] + dr, start_tile[1] + dc)
                    dist = (next_tile[0] - target_tile[0])**2 + (next_tile[1] - target_tile[1])**2
                    if dist < min_dist:
                        min_dist = dist
                        best_d = d
                        
                if best_d is None:
                    best_d = curr_d if curr_d != 0 else 3
                        
                curr_d = best_d
                ghst_drct[id][0] = curr_d
            
            if curr_d == 3 and ghost[id][0] == 12 * length and ghost[id][1] >= (board_x - 1) * length: 
                ghost[id][1] = 0
            elif curr_d == 9 and ghost[id][0] == 12 * length and ghost[id][1] <= 0: 
                ghost[id][1] = (board_x - 1) * length
            elif check(curr_d, ghost[id]):
                if curr_d == 3: ghost[id][1] += step
                elif curr_d == 6: ghost[id][0] += step
                elif curr_d == 9: ghost[id][1] -= step
                elif curr_d == 12: ghost[id][0] -= step
            print(target_tile, ghost[0], ghost[id])
                
            to_scrn(ghost[id], 5)

def main():
    global board, board_y, board_x, tab_y, tab_x, plyr, drct, old_drct, game_over
    pygame.init()
    pygame.display.set_caption("Pac-Man 005")
    screen = pygame.display.set_mode((tab_x, tab_y))
    clock = pygame.time.Clock()

    spawn()

    bg_plyr = threading.Thread(target=move, daemon=True)
    bg_red = threading.Thread(target=red, daemon=True)
    bg_pink = threading.Thread(target=pink, daemon=True)
    bg_blue = threading.Thread(target=blue, daemon=True)
    
    bg_plyr.start()
    bg_red.start()
    bg_pink.start()
    bg_blue.start()

    font_large = pygame.font.SysFont(None, 48)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    old_drct = drct
                    drct = 3
                if event.key == pygame.K_DOWN:
                    old_drct = drct
                    drct = 6
                if event.key == pygame.K_LEFT:
                    old_drct = drct
                    drct = 9
                if event.key == pygame.K_UP:
                    old_drct = drct
                    drct = 12

        with lock_plyr, lock_red, lock_pink, lock_blue:
            draw(screen)

        if game_over:
            overlay = pygame.Surface((tab_x, tab_y), pygame.SRCALPHA)
            overlay.fill((50, 50, 50, 160))
            screen.blit(overlay, (0, 0))

            text_surf = font_large.render("GAME OVER", True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(tab_x // 2, tab_y // 2))
            screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()