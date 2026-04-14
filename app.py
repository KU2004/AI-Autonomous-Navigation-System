import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import heapq
import time
from PIL import Image
import io

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="AI Navigation", page_icon="🤖", layout="wide")

st.title("🤖 AI Autonomous Navigation System")
st.markdown("### 🚀 Interactive Path Planning with Animation")

# -------------------------
# SESSION STATE
# -------------------------
if "grid" not in st.session_state:
    st.session_state.grid = None

if "start" not in st.session_state:
    st.session_state.start = (0, 0)

if "goal" not in st.session_state:
    st.session_state.goal = (9, 9)

if "path" not in st.session_state:
    st.session_state.path = None

# -------------------------
# A* ALGORITHM
# -------------------------
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    rows, cols = grid.shape
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            neighbor = (current[0]+dx, current[1]+dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor] == 1:
                    continue

                temp_g = g_score[current] + 1

                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    g_score[neighbor] = temp_g
                    f_score = temp_g + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor))
                    came_from[neighbor] = current

    return None

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("⚙️ Controls")

size = st.sidebar.slider("Grid Size", 5, 20, 10)

if st.session_state.grid is None or st.session_state.grid.shape != (size, size):
    st.session_state.grid = np.zeros((size, size))

mode = st.sidebar.radio("Mode", ["Obstacle", "Start", "Goal", "Erase"])

if st.sidebar.button("🧹 Clear Grid"):
    st.session_state.grid = np.zeros((size, size))
    st.session_state.path = None

if st.sidebar.button("🎲 Random Obstacles"):
    st.session_state.grid = np.random.choice([0,1], size=(size,size), p=[0.7,0.3])

# -------------------------
# CLICKABLE GRID
# -------------------------
st.subheader("🖱️ Click Grid to Modify")

cols = st.columns(size)

for i in range(size):
    cols = st.columns(size)
    for j in range(size):
        cell = cols[j].button(" ", key=f"{i}-{j}")

        if cell:
            if mode == "Obstacle":
                st.session_state.grid[i][j] = 1
            elif mode == "Erase":
                st.session_state.grid[i][j] = 0
            elif mode == "Start":
                st.session_state.start = (i, j)
            elif mode == "Goal":
                st.session_state.goal = (i, j)

# -------------------------
# VISUALIZATION FUNCTION
# -------------------------
def plot_grid(grid, path=None):
    fig, ax = plt.subplots()
    ax.imshow(grid)

    if path:
        x = [p[1] for p in path]
        y = [p[0] for p in path]
        ax.plot(x, y)

    ax.scatter(st.session_state.start[1], st.session_state.start[0])
    ax.scatter(st.session_state.goal[1], st.session_state.goal[0])

    ax.set_xticks([])
    ax.set_yticks([])

    return fig

# -------------------------
# DISPLAY GRID
# -------------------------
st.subheader("📊 Visualization")

fig = plot_grid(st.session_state.grid, st.session_state.path)
st.pyplot(fig)

# -------------------------
# RUN BUTTON
# -------------------------
if st.button("🚀 Find Path"):
    path = astar(st.session_state.grid, st.session_state.start, st.session_state.goal)

    if path:
        st.success("✅ Path Found!")
        st.session_state.path = path
    else:
        st.error("❌ No Path Found")

# -------------------------
# ANIMATION
# -------------------------
if st.session_state.path and st.checkbox("🎬 Show Animation"):
    st.subheader("🎥 Navigation Animation")

    for i in range(len(st.session_state.path)):
        partial_path = st.session_state.path[:i+1]
        fig = plot_grid(st.session_state.grid, partial_path)
        st.pyplot(fig)
        time.sleep(0.2)

# -------------------------
# METRICS
# -------------------------
if st.session_state.path:
    st.markdown("### 📈 Metrics")
    st.info(f"Path Length: {len(st.session_state.path)} steps")

# -------------------------
# DOWNLOAD IMAGE
# -------------------------
if st.session_state.path:
    fig = plot_grid(st.session_state.grid, st.session_state.path)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("📥 Download Result", buf.getvalue(), "navigation.png")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("🔥 Advanced AI Navigation System | Streamlit App")