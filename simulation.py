import numpy as np

def create_grid(size=10):
    """
    Create grid with:
    - User-defined obstacles
    - User-defined start & goal
    """

    grid = np.zeros((size, size))

    print(f"\n🧩 Grid Size: {size}x{size}")

    # -----------------------------
    # 🔹 STEP 1: Obstacles Input
    # -----------------------------
    print("\n👉 Enter obstacle positions (row col)")
    print("👉 Type 'done' when finished\n")

    while True:
        user_input = input("Obstacle (row col): ")

        if user_input.lower() == "done":
            break

        try:
            x, y = map(int, user_input.split())

            if 0 <= x < size and 0 <= y < size:
                grid[x][y] = 1
            else:
                print("⚠️ Out of bounds. Try again.")

        except:
            print("⚠️ Invalid format. Use: row col")

    # -----------------------------
    # 🔹 STEP 2: Start Position
    # -----------------------------
    while True:
        try:
            start_input = input("\n🟢 Enter START position (row col): ")
            sx, sy = map(int, start_input.split())

            if not (0 <= sx < size and 0 <= sy < size):
                print("⚠️ Out of bounds.")
                continue

            if grid[sx][sy] == 1:
                print("⚠️ Start cannot be on obstacle.")
                continue

            start = (sx, sy)
            break

        except:
            print("⚠️ Invalid format. Use: row col")

    # -----------------------------
    # 🔹 STEP 3: Goal Position
    # -----------------------------
    while True:
        try:
            goal_input = input("\n🔴 Enter GOAL position (row col): ")
            gx, gy = map(int, goal_input.split())

            if not (0 <= gx < size and 0 <= gy < size):
                print("⚠️ Out of bounds.")
                continue

            if grid[gx][gy] == 1:
                print("⚠️ Goal cannot be on obstacle.")
                continue

            goal = (gx, gy)
            break

        except:
            print("⚠️ Invalid format. Use: row col")

    return grid, start, goal