# Project 3 Reflection

## What I Learned

This project helped me understand the basic principles behind autonomous mobile robot navigation.

I learned how simulated LiDAR measurements can be used to identify obstacles and how the information can be represented using a 2D occupancy grid.

I also implemented the A* pathfinding algorithm using the Manhattan distance heuristic to find a route from the robot's starting position to its destination.

## Dynamic Obstacle Handling

One of the most important parts of the project was handling an unexpected obstacle.

During testing, an obstacle was introduced directly onto the robot's original path. The robot detected the change, stopped safely, and the system calculated an alternative route using A*.

## Challenges

One challenge was designing the occupancy grid and ensuring that the pathfinding algorithm did not move through occupied cells.

Another challenge was making the dynamic obstacle affect the existing route and then successfully calculating a new route.

## Result

The completed simulation successfully demonstrated:

- Simulated LiDAR mapping
- 2D occupancy grid generation
- A* pathfinding
- Manhattan distance heuristic
- Dynamic obstacle detection
- Automatic path re-planning

The initial route contained 39 cells. After the dynamic obstacle was introduced, the system successfully calculated an alternative route.

## Conclusion

This project improved my understanding of how sensing, mapping, path planning, and obstacle avoidance work together in an autonomous navigation system.

It also gave me practical experience implementing a navigation algorithm rather than only studying the theory.