from collections import deque
import numpy as np
from config_minimap import MAZE_STR
maze = np.array([[int(char) for char in row] for row in MAZE_STR.strip().splitlines()])
def shortestPath(src, dest):
    mat = maze
    n = len(mat)
    m = len(mat[0])
    if mat[src[0]][src[1]] == 1 or mat[dest[0]][dest[1]] == 1:
        return -1
    q = deque()
    q.append((src[0], src[1]))
    parent = {(src[0], src[1]): None}
    visited = {(src[0], src[1])}
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    while q:
        x, y = q.popleft()
        if x == dest[0] and y == dest[1]:
            path = []
            curr = (x, y)
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < n and 0 <= ny < m and mat[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                q.append((nx, ny))

    return -1