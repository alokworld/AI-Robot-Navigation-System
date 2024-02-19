from queue import Queue

class RobotNavigation:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]

    def set_obstacle(self, row, col):
        self.grid[row][col] = '#'

    def set_goal(self, row, col):
        self.grid[row][col] = 'G'

    def set_start(self, row, col):
        self.grid[row][col] = 'S'

    def is_valid_move(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] != '#'

    def bfs(self, start, goal):
        queue = Queue()
        visited = []

        queue.put(start)
        visited.append(start)

        while not queue.empty():
            current_row, current_col, path = queue.get()

            if (current_row, current_col) == goal:
                return path

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

            for dr, dc in directions:
                new_row, new_col = current_row + dr, current_col + dc
                if self.is_valid_move(new_row, new_col) and (new_row, new_col) not in visited:
                    queue.put((new_row, new_col, path + [(new_row, new_col)]))
                    visited.append((new_row, new_col))

        return None

    def display_grid(self, path=None):
        for row in self.grid:
            print(' '.join(row))
        if path:
            print("\nOptimal Path:")
            for row, col in path:
                self.grid[row][col] = '*'
            for row in self.grid:
                print(' '.join(row))

robot_nav = RobotNavigation(rows=5, cols=5)
robot_nav.set_start(0, 0)
robot_nav.set_goal(4, 4)
robot_nav.set_obstacle(1, 2)
robot_nav.set_obstacle(2, 2)
robot_nav.set_obstacle(3, 2)

start = (0, 0, [(0, 0)])
goal = (4, 4)

optimal_path = robot_nav.bfs(start, goal)
robot_nav.display_grid(optimal_path)
