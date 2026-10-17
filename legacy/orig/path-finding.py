# Directions: Down, Left, Right, Up
dir = "DLRU"
dr = [1, 0, 0, -1]
dc = [0, -1, 1, 0]


# Check if a cell is valid (inside the maze and open)
def isValid(r, c, n, maze):
    return r >= 0 and c >= 0 and r < n and c < n and maze[r][c] == 1


# Function to find all valid paths
def findPath(r, c, maze, path, res):
    n = len(maze)

    # If destination is reached, store the path
    if r == n - 1 and c == n - 1:
        res.append("".join(path))
        return

    # Mark current cell as visited
    maze[r][c] = 0

    for i in range(4):
        nr, nc = r + dr[i], c + dc[i]
        if isValid(nr, nc, n, maze):
            path.append(dir[i])

            # Move to the next cell recursively
            findPath(nr, nc, maze, path, res)

            # Backtrack
            path.pop()

    # Unmark current cell
    maze[r][c] = 1


# Function to find all paths and return them
def ratInMaze(maze):
    result = []
    n = len(maze)
    path = []

    if maze[0][0] == 1 and maze[n - 1][n - 1] == 1:
        # Start from (0,0)
        findPath(0, 0, maze, path, result)

    # Sort results lexicographically
    result.sort()

    return result


if __name__ == "__main__":
    maze = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 1, 0, 0],
        [0, 1, 1, 1]
    ]

    result = ratInMaze(maze)
    result_string=""
    for p in result:
        print(p, end=" ")