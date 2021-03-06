from heapq import heappop, heappush
from structs import Point, TileContent
from actions import create_move_action

def dist(p1, p2):
    return abs(p1.X - p2.X) +  abs(p1.Y - p2.Y)

def free(tiles, p, player):
    """
    p has absolute coordinates
    """
    # Change start and stop to relative coordinates
    x = p.X - 10 + player.X
    y = p.Y - 10 + player.Y

    if x < 0:
        return False
    if y < 0:
        return False
    if x >= 19:
        return False
    if y >= 19:
        return False
    # TODO: prevent overflows
    if tiles[x][y].Content != TileContent.Empty:
        return False
    return True

def find_path(tiles, start, goal, player):
    """
    Search for the minimal path from start to an adjacent cell of goal
    start and stop are absolute coordinates in the full map.
    """
    def heuristic(cell, goal):
        return dist(cell, goal) - 1

    pr_queue = []
    #heappush(pr_queue, (0 + heuristic(start, goal), 0, start, start))
    right = Point(start.X - 1, start.Y)
    if free(tiles, right, player):
        heappush(pr_queue, (0 + heuristic(right, goal), 0, right, right))
    left = Point(start.X + 1, start.Y)
    if free(tiles, left, player):
        heappush(pr_queue, (0 + heuristic(left, goal), 0, left, left))
    up = Point(start.X , start.Y - 1)
    if free(tiles, up, player):
        heappush(pr_queue, (0 + heuristic(up, goal), 0, up, up))
    down = Point(start.X , start.Y + 1)
    if free(tiles, down, player):
        heappush(pr_queue, (0 + heuristic(down, goal), 0, down, down))
    visited = {start}

    while pr_queue:
        _, cost, path, current = heappop(pr_queue)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        right = Point(current.X - 1, current.Y)
        if free(tiles, right, player):
            heappush(pr_queue, (cost + heuristic(right, goal), cost + 1, path, right))
        left = Point(current.X + 1, current.Y)
        if free(tiles, left, player):
            heappush(pr_queue, (cost + heuristic(left, goal), cost + 1, path, left))
        up = Point(current.X , current.Y - 1)
        if free(tiles, up, player):
            heappush(pr_queue, (cost + heuristic(up, goal), cost + 1, path, up))
        down = Point(current.X , current.Y + 1)
        if free(tiles, down, player):
            heappush(pr_queue, (cost + heuristic(down, goal), cost + 1, path, down))
    return None

def move_to(tiles, start, goal, player):
    p = find_path(tiles, start, goal, player)
    if p != None:
        return create_move_action(p)
    return None

