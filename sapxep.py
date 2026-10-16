from collections import deque

class PuzzleNode:
    def __init__(self, state, goal_state, parent=None, action=None):
        self.state = state          
        self.goal_state = goal_state 
        self.parent = parent        
        self.action = action        

def get_blank_pos(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_next_nodes(node):
    neighbors = []
    r, c = get_blank_pos(node.state)
    
    moves = [ 
    ( 0,  1, "RIGHT", "LEFT"),
    (-1,  0, "UP", "DOWN"), 
    ( 1,  0, "DOWN", "UP"), 
    ( 0, -1, "LEFT", "RIGHT") 
    ]
    
    for dr, dc, action, inverse_action in moves:
        if node.action == inverse_action:
            continue
            
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [list(row) for row in node.state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            tuple_state = tuple(tuple(row) for row in new_state)
            
            child = PuzzleNode(
                state=tuple_state,
                goal_state=node.goal_state,
                parent=node,
                action=action
            )
            neighbors.append(child)
            
    return neighbors

def solve_puzzle_bfs(start_state, goal_state):
    """Giải bài toán 8-puzzle bằng Tìm kiếm theo chiều rộng (BFS)"""
    root = PuzzleNode(state=start_state, goal_state=goal_state)
    
    # Hàng đợi cho BFS
    queue = deque([root])
    
    # Tập hợp quản lý các trạng thái đã duyệt qua để chống lặp vô tận
    visited = {start_state}

    while queue:
        current_node = queue.popleft()
        
        # Kiểm tra nếu đã đến đích
        if current_node.state == goal_state:
            path = []
            curr = current_node
            while curr.parent is not None:
                path.append((curr.action, curr.state))
                curr = curr.parent
            return path[::-1]
            
        for neighbor in get_next_nodes(current_node):
            if neighbor.state not in visited:
                visited.add(neighbor.state)
                queue.append(neighbor)
                
    return None 

if __name__ == "__main__":
    CUSTOM_START = (
        (2, 1, 4),
        (3, 0, 6),
        (7, 5, 8)
    )
    
    CUSTOM_GOAL = (
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 0)
    )
    
    print("Đang tìm lời giải bằng BFS (Tìm kiếm theo chiều rộng)...")
    solution = solve_puzzle_bfs(CUSTOM_START, CUSTOM_GOAL)
    
    if solution:
        print(f"Thành công! Tìm thấy đường đi gồm {len(solution)} bước:\n")
        for i, (action, state) in enumerate(solution, 1):
            print(f"Bước {i} - Hướng đi ô trống: {action}")
            for row in state:
                print("  ", [x if x != 0 else ' ' for x in row])
            print("-" * 25)
    else:
        print("Trạng thái này không thể giải được (unsolvable)!")