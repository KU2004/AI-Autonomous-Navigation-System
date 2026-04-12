from src.simulation import create_grid
from src.path_planning import astar
from src.visualization import visualize_path

def main():
    grid, start, goal = create_grid()

    path = astar(grid, start, goal)

    if path:
        print("Path Found!")
        visualize_path(grid, path)
    else:
        print("No Path Found")

if __name__ == "__main__":
    main()