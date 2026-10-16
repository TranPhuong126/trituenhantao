from collections import deque

class Node:
    def __init__(self, pos, parent=None, action=None):
        self.pos = pos
        self.parent = parent
        self.action = action

class MazeSolver:
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.moves = [
            (-1, 0, "RIGHT"),
            (1, 0, "LEFT"),
            (0, -1, "UP"),
            (0, 1, "DOWN")
        ]

    def is_valid(self, r, c, visited):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        return self.maze[r][c] == 0 and (r, c) not in visited

    def solve(self):
        root = Node(pos=self.start)
        queue = deque([root])
        visited = {self.start}

        while queue:
            current_node = queue.popleft()
            if current_node.pos == self.goal:
                return self._reconstruct_path(current_node)

            r, c = current_node.pos
            for dr, dc, action in self.moves:
                nr, nc = r + dr, c + dc
                if self.is_valid(nr, nc, visited):
                    visited.add((nr, nc))
                    queue.append(Node(pos=(nr, nc), parent=current_node, action=action))
        return None

    def _reconstruct_path(self, node):
        path = []
        curr = node
        while curr.parent is not None:
            path.append((curr.action, curr.pos))
            curr = curr.parent
        return path[::-1]

if __name__ == "__main__":
    MAZE_DATA = [
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
    ]

    START_POS = (3, 0)
    GOAL_POS = (0, 3)

    solver = MazeSolver(MAZE_DATA, START_POS, GOAL_POS)
    path = solver.solve()

    if path:
        print("CÁC BƯỚC DI CHUYỂN:")
        for i, (action, pos) in enumerate(path, 1):
            print(f"Bước {i}: {action} -> Tọa độ {pos}")

        print("\nSƠ ĐỒ MÊ CUNG:")
        rows = len(MAZE_DATA)
        cols = len(MAZE_DATA[0])
        display_grid = [["." for _ in range(cols)] for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                if MAZE_DATA[r][c] == 1:
                    display_grid[r][c] = "X"

        for _, pos in path:
            display_grid[pos[0]][pos[1]] = "*"

        display_grid[START_POS[0]][START_POS[1]] = "S"
        display_grid[GOAL_POS[0]][GOAL_POS[1]] = "G"

        for row in display_grid:
            print(" | ".join(row))
    else:
        print("Không tìm thấy đường đi!")