import heapq

# ============================================================
# DECODELABS PROJECT 3
# Autonomous Mobile Robot (AMR) Navigation
#
# Features:
# 1. Simulated LiDAR
# 2. 2D Occupancy Grid
# 3. A* Pathfinding
# 4. Manhattan Distance Heuristic
# 5. Dynamic Obstacle Detection
# 6. Automatic Path Re-planning
# ============================================================


# ------------------------------------------------------------
# 1. ENVIRONMENT
# ------------------------------------------------------------

ROWS = 20
COLS = 20

# 0 = free space
# 1 = occupied space / obstacle
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]


# Static walls/obstacles in the simulated environment
static_obstacles = [
    (4, 4), (4, 5), (4, 6), (4, 7),
    (8, 2), (9, 2), (10, 2), (11, 2),
    (12, 8), (12, 9), (12, 10), (12, 11),
    (6, 14), (7, 14), (8, 14), (9, 14),
    (15, 4), (15, 5), (15, 6)
]

for row, col in static_obstacles:
    grid[row][col] = 1


# ------------------------------------------------------------
# 2. SIMULATED LiDAR
# ------------------------------------------------------------

def simulate_lidar(robot_position, max_range=5):

    detected_obstacles = []

    robot_row, robot_col = robot_position

    # LiDAR scans eight directions
    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1),    # Right
        (-1, -1),  # Up-left
        (-1, 1),   # Up-right
        (1, -1),   # Down-left
        (1, 1)     # Down-right
    ]

    for direction_row, direction_col in directions:

        for distance in range(1, max_range + 1):

            new_row = robot_row + direction_row * distance
            new_col = robot_col + direction_col * distance

            # Stop scanning outside the map
            if (
                new_row < 0
                or new_row >= ROWS
                or new_col < 0
                or new_col >= COLS
            ):
                break

            # Stop when an obstacle is detected
            if grid[new_row][new_col] == 1:

                detected_obstacles.append(
                    (new_row, new_col)
                )

                break

    return detected_obstacles


# ------------------------------------------------------------
# 3. OCCUPANCY GRID UPDATE
# ------------------------------------------------------------

def update_occupancy_grid(lidar_data):

    for row, col in lidar_data:

        grid[row][col] = 1


# ------------------------------------------------------------
# 4. MANHATTAN DISTANCE HEURISTIC
# ------------------------------------------------------------

def manhattan_distance(current, goal):

    return (
        abs(current[0] - goal[0])
        + abs(current[1] - goal[1])
    )


# ------------------------------------------------------------
# 5. GET VALID NEIGHBOURS
# ------------------------------------------------------------

def get_neighbors(node):

    row, col = node

    movements = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    neighbors = []

    for move_row, move_col in movements:

        new_row = row + move_row
        new_col = col + move_col

        # Check map boundaries
        if (
            0 <= new_row < ROWS
            and 0 <= new_col < COLS
        ):

            # Only allow free cells
            if grid[new_row][new_col] == 0:

                neighbors.append(
                    (new_row, new_col)
                )

    return neighbors


# ------------------------------------------------------------
# 6. A* PATHFINDING
# ------------------------------------------------------------

def astar(start, goal):

    # Priority queue
    open_list = []

    # Start node
    heapq.heappush(
        open_list,
        (0, start)
    )

    # Stores previous node
    came_from = {}

    # Cost from start
    cost_so_far = {
        start: 0
    }

    while open_list:

        current_priority, current = heapq.heappop(
            open_list
        )

        # Goal reached
        if current == goal:

            path = []

            while current in came_from:

                path.append(current)

                current = came_from[current]

            path.append(start)

            path.reverse()

            return path

        # Explore neighbours
        for neighbor in get_neighbors(current):

            new_cost = (
                cost_so_far[current] + 1
            )

            # New or better route
            if (
                neighbor not in cost_so_far
                or new_cost < cost_so_far[neighbor]
            ):

                cost_so_far[neighbor] = new_cost

                priority = (
                    new_cost
                    + manhattan_distance(
                        neighbor,
                        goal
                    )
                )

                heapq.heappush(
                    open_list,
                    (priority, neighbor)
                )

                came_from[neighbor] = current

    # No route found
    return []


# ------------------------------------------------------------
# 7. DYNAMIC OBSTACLE
# ------------------------------------------------------------

def add_dynamic_obstacle(position):

    row, col = position

    grid[row][col] = 1


# ------------------------------------------------------------
# 8. PRINT OCCUPANCY GRID
# ------------------------------------------------------------

def print_grid(path=None, robot=None, goal=None):

    print()
    print("2D OCCUPANCY GRID")
    print("------------------")

    path_set = set(path) if path else set()

    for row in range(ROWS):

        line = ""

        for col in range(COLS):

            position = (row, col)

            if robot == position:

                symbol = "R"

            elif goal == position:

                symbol = "G"

            elif grid[row][col] == 1:

                symbol = "#"

            elif position in path_set:

                symbol = "*"

            else:

                symbol = "."

            line += symbol + " "

        print(line)

    print()
    print("Legend:")
    print("R = Robot")
    print("G = Goal")
    print("# = Obstacle")
    print("* = Planned path")
    print(". = Free space")
    print()


# ------------------------------------------------------------
# 9. MAIN AUTONOMOUS NAVIGATION
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("DECODELABS PROJECT 3")
    print("AUTONOMOUS MOBILE ROBOT (AMR) NAVIGATION")
    print("=" * 60)

    # Robot starting position
    robot = (0, 0)

    # Navigation goal
    goal = (19, 19)

    print()
    print("Robot Start Position:", robot)
    print("Navigation Goal:", goal)

    # --------------------------------------------------------
    # LiDAR scan
    # --------------------------------------------------------

    print()
    print("STEP 1: SIMULATED LiDAR SCAN")

    lidar_data = simulate_lidar(
        robot,
        max_range=5
    )

    print(
        "LiDAR detected obstacles:",
        lidar_data
    )

    # --------------------------------------------------------
    # Occupancy grid
    # --------------------------------------------------------

    print()
    print("STEP 2: OCCUPANCY GRID MAPPING")

    update_occupancy_grid(
        lidar_data
    )

    print("Occupancy grid updated successfully.")

    print_grid(
        robot=robot,
        goal=goal
    )

    # --------------------------------------------------------
    # Initial A* route
    # --------------------------------------------------------

    print()
    print("STEP 3: A* PATH PLANNING")

    initial_path = astar(
        robot,
        goal
    )

    if not initial_path:

        print("ERROR: No initial path found.")

        return

    print(
        "Initial path found successfully."
    )

    print(
        "Initial path length:",
        len(initial_path)
    )

    print_grid(
        path=initial_path,
        robot=robot,
        goal=goal
    )

    # --------------------------------------------------------
    # Dynamic obstacle
    # --------------------------------------------------------

    print()
    print("STEP 4: DYNAMIC OBSTACLE DETECTION")

    # Place an unexpected obstacle
    # directly on the planned route.
    dynamic_position = initial_path[5]

    print(
        "Unexpected obstacle detected at:",
        dynamic_position
    )

    add_dynamic_obstacle(
        dynamic_position
    )

    print(
        "Robot stopped safely."
    )

    # --------------------------------------------------------
    # Re-plan
    # --------------------------------------------------------

    print()
    print("STEP 5: DYNAMIC PATH RE-PLANNING")

    new_path = astar(
        robot,
        goal
    )

    if not new_path:

        print(
            "No alternative route is available."
        )

        return

    print(
        "Alternative route calculated successfully."
    )

    print(
        "New path length:",
        len(new_path)
    )

    print_grid(
        path=new_path,
        robot=robot,
        goal=goal
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("=" * 60)
    print("NAVIGATION RESULT")
    print("=" * 60)

    print(
        "LiDAR Mapping: SUCCESS"
    )

    print(
        "Occupancy Grid: SUCCESS"
    )

    print(
        "A* Pathfinding: SUCCESS"
    )

    print(
        "Manhattan Heuristic: SUCCESS"
    )

    print(
        "Dynamic Obstacle Detection: SUCCESS"
    )

    print(
        "Automatic Re-routing: SUCCESS"
    )

    print()
    print(
        "AMR NAVIGATION SIMULATION COMPLETED SUCCESSFULLY."
    )

    print("=" * 60)


# ------------------------------------------------------------
# PROGRAM START
# ------------------------------------------------------------

if __name__ == "__main__":

    main()