directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

def bfs(start, end, grid):
    queue = [start]
    visited = {start}

    while queue:
        current = queue.pop(-1)
        if current == end:
            return True
        for direction in directions:
            next_cell = (current[0] + direction[0], current[1] + direction[1])
            if next_cell not in visited and grid[next_cell[0]][next_cell[1]] != "#":
                visited.add(next_cell)
                queue.append(next_cell)
    return False