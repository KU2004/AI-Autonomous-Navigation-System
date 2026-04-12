import matplotlib.pyplot as plt

def visualize_path(grid, path):
    plt.imshow(grid, cmap='gray')

    x = [p[1] for p in path]
    y = [p[0] for p in path]

    plt.plot(x, y, color='blue', linewidth=2)

    plt.title("Autonomous Navigation Path")
    plt.show()