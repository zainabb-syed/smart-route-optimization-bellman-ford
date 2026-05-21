import tkinter as tk
from tkinter import ttk

# =========================================================
# Bellman Ford Algorithm
# =========================================================


def bellman_ford(vertices, edges, source):

    distance = {}
    predecessor = {}

    # Initialize distances
    for vertex in vertices:

        distance[vertex] = float("inf")
        predecessor[vertex] = None

    distance[source] = 0

    # Relax all edges |V| - 1 times
    for _ in range(len(vertices) - 1):

        updated = False

        for u, v, weight in edges:

            if distance[u] != float("inf") and distance[u] + weight < distance[v]:

                distance[v] = distance[u] + weight
                predecessor[v] = u
                updated = True

        if not updated:
            break

    # Negative Cycle Detection
    for u, v, weight in edges:

        if distance[u] != float("inf") and distance[u] + weight < distance[v]:

            return None, None

    return distance, predecessor


# =========================================================
# Generate Path
# =========================================================


def generate_path(predecessor, source, destination):

    path = []
    current = destination

    while current is not None:

        path.insert(0, current)
        current = predecessor[current]

    if len(path) == 0 or path[0] != source:
        return None

    return path


# =========================================================
# Animate Route
# =========================================================


def animate_route(route, index=0):

    if index >= len(route) - 1:
        return

    city1 = route[index]
    city2 = route[index + 1]

    x1, y1 = city_positions[city1]
    x2, y2 = city_positions[city2]

    offset = 80

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2 - offset

    canvas.create_line(
        x1,
        y1,
        mid_x,
        mid_y,
        x2,
        y2,
        smooth=True,
        splinesteps=100,
        width=6,
        fill="#00cec9",
        tags="highlight",
    )

    root.after(500, lambda: animate_route(route, index + 1))


# =========================================================
# Highlight Cities
# =========================================================


def highlight_nodes(source, destination):

    for city in [source, destination]:

        x, y = city_positions[city]

        canvas.create_oval(
            x - 40, y - 40, x + 40, y + 40, outline="#f1c40f", width=5, tags="highlight"
        )


# =========================================================
# Traffic Analysis
# =========================================================


def traffic_status(distance):

    if distance <= 4:
        return "Low Traffic", "#2ecc71"

    elif distance <= 8:
        return "Moderate Traffic", "#f39c12"

    else:
        return "High Traffic", "#e74c3c"


# =========================================================
# Find Route
# =========================================================


def find_route():

    canvas.delete("highlight")

    source = source_var.get()
    destination = destination_var.get()

    # Same source & destination
    if source == destination:

        result_label.config(text="Source and Destination Cannot Be Same", fg="orange")

        return

    # Run Bellman Ford
    distances, predecessors = bellman_ford(cities, graph, source)

    # Negative cycle
    if distances is None:

        result_label.config(text="Negative Weight Cycle Detected", fg="red")

        return

    # No path available
    if distances[destination] == float("inf"):

        result_label.config(text="No Route Available", fg="red")

        return

    # Generate shortest path
    route = generate_path(predecessors, source, destination)

    if route is None:

        result_label.config(text="Path Generation Failed", fg="red")

        return

    path_string = " → ".join(route)

    shortest_distance = distances[destination]

    status, color = traffic_status(shortest_distance)

    result_label.config(
        text=f"Shortest Distance : {shortest_distance} km\n\n"
        f"Optimized Path :\n{path_string}\n\n"
        f"Traffic Status : {status}",
        fg=color,
    )

    animate_route(route)

    highlight_nodes(source, destination)


# =========================================================
# Cities
# =========================================================

cities = ["Bangalore", "Hyderabad", "Chennai", "Mumbai", "Delhi", "Pune", "Kolkata"]


# =========================================================
# Graph Edges
# =========================================================

graph = [
    ("Bangalore", "Hyderabad", 4),
    ("Bangalore", "Chennai", 2),
    ("Chennai", "Hyderabad", 1),
    ("Chennai", "Mumbai", 7),
    ("Hyderabad", "Mumbai", 2),
    ("Hyderabad", "Delhi", 6),
    ("Mumbai", "Pune", 3),
    ("Pune", "Delhi", 2),
    ("Delhi", "Kolkata", -5),
    ("Kolkata", "Mumbai", 4),
]


# =========================================================
# GUI Window
# =========================================================

root = tk.Tk()

root.title("Smart Route Optimization System")
root.geometry("1450x780")
root.config(bg="#0f172a")


# =========================================================
# Heading
# =========================================================

heading = tk.Label(
    root,
    text="Smart Route Optimization System",
    font=("Segoe UI", 34, "bold"),
    bg="#0f172a",
    fg="white",
)

heading.pack(pady=20)


# =========================================================
# Main Frame
# =========================================================

main_frame = tk.Frame(root, bg="#0f172a")

main_frame.pack(fill="both", expand=True)


# =========================================================
# Sidebar
# =========================================================

sidebar = tk.Frame(main_frame, bg="#1e293b", width=330)

sidebar.pack(side="left", fill="y", padx=20, pady=20)


# =========================================================
# Source Dropdown
# =========================================================

source_var = tk.StringVar()
source_var.set(cities[0])

source_label = tk.Label(
    sidebar, text="Source City", font=("Arial", 15, "bold"), bg="#1e293b", fg="white"
)

source_label.pack(pady=(40, 10))

source_menu = ttk.Combobox(
    sidebar,
    textvariable=source_var,
    values=cities,
    state="readonly",
    width=24,
    font=("Arial", 12),
)

source_menu.pack(pady=10)


# =========================================================
# Destination Dropdown
# =========================================================

destination_var = tk.StringVar()
destination_var.set(cities[1])

destination_label = tk.Label(
    sidebar,
    text="Destination City",
    font=("Arial", 15, "bold"),
    bg="#1e293b",
    fg="white",
)

destination_label.pack(pady=(30, 10))

destination_menu = ttk.Combobox(
    sidebar,
    textvariable=destination_var,
    values=cities,
    state="readonly",
    width=24,
    font=("Arial", 12),
)

destination_menu.pack(pady=10)


# =========================================================
# Find Route Button
# =========================================================

find_button = tk.Button(
    sidebar,
    text="Find Optimized Route",
    command=find_route,
    bg="#7c3aed",
    fg="white",
    activebackground="#6d28d9",
    font=("Arial", 14, "bold"),
    width=20,
    height=2,
    bd=0,
    cursor="hand2",
)

find_button.pack(pady=40)


# =========================================================
# Result Label
# =========================================================

result_label = tk.Label(
    sidebar,
    text="Route Details",
    font=("Arial", 14, "bold"),
    bg="#1e293b",
    fg="#2ecc71",
    justify="left",
    wraplength=280,
)

result_label.pack(pady=20)


# =========================================================
# Canvas Frame
# =========================================================

canvas_frame = tk.Frame(main_frame, bg="#0f172a")

canvas_frame.pack(side="right", fill="both", expand=True)


# =========================================================
# Canvas
# =========================================================

canvas = tk.Canvas(
    canvas_frame, width=1100, height=650, bg="#ecf0f1", bd=5, relief="ridge"
)

canvas.pack(padx=20, pady=20)


# =========================================================
# Updated City Positions
# =========================================================

city_positions = {
    "Mumbai": (180, 300),
    "Pune": (420, 130),
    "Delhi": (700, 120),
    "Kolkata": (980, 260),
    "Hyderabad": (550, 330),
    "Bangalore": (300, 580),
    "Chennai": (850, 580),
}

# =========================================================
# Draw Graph Edges
# =========================================================

for index, (u, v, weight) in enumerate(graph):

    x1, y1 = city_positions[u]
    x2, y2 = city_positions[v]

    # Alternate curve directions
    if index % 2 == 0:
        offset = 80
    else:
        offset = -80

    # Midpoint
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2 + offset

    # Draw curved edge
    canvas.create_line(
        x1,
        y1,
        mid_x,
        mid_y,
        x2,
        y2,
        smooth=True,
        splinesteps=100,
        width=3,
        fill="#636e72",
        arrow=tk.LAST,
    )

    # Weight position
    weight_x = (x1 + x2 + mid_x) / 3
    weight_y = (y1 + y2 + mid_y) / 3

    # Draw weight
    canvas.create_text(
        weight_x, weight_y, text=str(weight), font=("Arial", 11, "bold"), fill="black"
    )
# =========================================================
# Draw Cities
# =========================================================

for city, (x, y) in city_positions.items():

    canvas.create_oval(x - 35, y - 35, x + 35, y + 35, fill="#6c5ce7", outline="")

    canvas.create_text(x, y, text=city, fill="white", font=("Arial", 11, "bold"))


# =========================================================
# Footer
# =========================================================

footer = tk.Label(
    root,
    text="Bellman Ford Algorithm Based Smart Route Optimization",
    font=("Arial", 11),
    bg="#0f172a",
    fg="lightgray",
)

footer.pack(pady=5)


# =========================================================
# Run Application
# =========================================================

root.mainloop()
