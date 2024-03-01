from queue import Queue
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import sqlite3

class RobotNavigation:
    def __init__(self, rows, cols, db_filename="robot_navigation.db"):
        self.rows = rows
        self.cols = cols
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.db_filename = db_filename
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Grid (
                row INTEGER,
                col INTEGER,
                value TEXT
            )
        ''')
        self.cursor.execute('''
            INSERT INTO Grid (row, col, value)
            VALUES (?, ? , "G")
        ''',(rows-1,cols-1))
                
            
        self.connection.commit()


    def set_obstacle(self, row, col):
        self.cursor.execute('''
            INSERT INTO Grid (row, col, value)
            VALUES (?, ?, "X")
        ''', (row, col))
        self.connection.commit()

    def set_start(self, row, col):
        self.cursor.execute('''
            INSERT INTO Grid (row, col, value)
            VALUES (0, 0, "S")
        ''')
        self.connection.commit()

    def is_valid_move(self, row, col):
        target_r = row
        target_c = col
        target_v = "X"

        query = f"SELECT * FROM Grid WHERE row = ? AND col = ? AND value = ?"
        self.cursor.execute(query, (target_r, target_c, target_v))
        result = self.cursor.fetchall()
        self.connection.commit()
        return 0 <= row < self.rows and 0 <= col < self.cols and not result

    def dfs(self, start, goal):
        stack=[]
        visited = set() 

        stack.append(start)

        while not len(stack)==0:
            current_row, current_col = stack.pop()
            if (current_row, current_col) not in visited:
                visited.add((current_row, current_col))

                if (current_row, current_col) == goal:
                    return visited

                directions = [(0, 1), (1, 0)] 

                for dr, dc in directions:
                    new_row, new_col = current_row + dr, current_col + dc
                    if self.is_valid_move(new_row, new_col) and (new_row, new_col) not in visited:
                        stack.append((new_row, new_col))

        return set()

    def truncate(self):
        self.cursor.execute('''drop table Grid''')
        self.connection.commit()


robot_nav = RobotNavigation(rows=5, cols=5)
obs=[]       
print("Do you want create a New Map \nYes: 1\nNo: 0")
i=int(input())
if i:
    query = f"DELETE FROM Grid"
    robot_nav.cursor.execute(query)
    robot_nav.connection.commit()
    print("Enter No. of Obstacles:")
    n=int(input())
    for i in range(n):
        print("Enter Row")
        r=int(input())
        print("Enter Cols")
        c=int(input())
        robot_nav.set_obstacle(r,c)
        obs.append((r,c))

else:
        query = f"DELETE FROM Grid"
        robot_nav.cursor.execute(query)
        #Default Map
        robot_nav.set_obstacle(0, 1)
        robot_nav.set_obstacle(0, 2)
        robot_nav.set_obstacle(0, 3)
        robot_nav.set_obstacle(1, 1)
        robot_nav.set_obstacle(1, 2)
        robot_nav.set_obstacle(1, 4)
        robot_nav.set_obstacle(1, 3)
        robot_nav.set_obstacle(3, 1)
        robot_nav.set_obstacle(3, 0)
        obs = [(0, 1), (0, 2), (0, 3), (1, 1), (1,2), (1, 3), (1,4), (3,0), (3,1)]

robot_nav.set_start(0, 0)

start = (0, 0)
goal = (4, 4)

optimal_path = robot_nav.dfs(start, goal)

if len(optimal_path) != 0:
    print(type(optimal_path))
    print(optimal_path)
    x_coords, y_coords = zip(*optimal_path)

    # Plot the points
    plt.scatter(x_coords, y_coords)

else:
    print("No Path Exists!!!")

for i, point in enumerate(obs):
    plt.text(point[0], point[1], 'X', ha='right', va='bottom', fontweight='bold')

plt.text(0, 0, 'S', ha='right', va='bottom', fontweight='bold')
plt.text(4, 4, 'G', ha='right', va='bottom', fontweight='bold')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))


plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('AI Navigation Map')
plt.grid(True)
plt.show()
