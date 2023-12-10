import networkx as nx
import turtle
from tkinter import messagebox, simpledialog

class DFSVisualizer:
    def __init__(self, graph):
        self.graph = graph
        self.visited_nodes = set()
        self.path = []
        self.paused = False
        self.goal_node = None  # Initialize goal node as None
        self.goal_reached = False  # Track whether the goal node has been reached

        self.screen = turtle.Screen()
        self.screen.bgcolor("white")
        self.screen.title("DFS Visualizer")

        self.node_turtles = {}
        self.edge_turtles = {}
        self.create_turtles()

        self.screen.listen()
        self.screen.onkey(self.toggle_pause, "space")  # Register the space bar to toggle pause

        self.enqueue_count = 0  # Initialize enqueue counter
        self.queue_size = 0  # Initialize queue size

    def create_turtles(self):
        pos = nx.spring_layout(self.graph)
        for node in self.graph.nodes:
            x, y = pos[node]
            turtle_node = turtle.Turtle()
            turtle_node.penup()
            turtle_node.goto(x * 200, y * 200)
            turtle_node.dot(20, 'skyblue')
            turtle_node.write(str(node), align='right', font=('Arial', 20, 'normal'))
            self.node_turtles[node] = turtle_node

        for edge in self.graph.edges:
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            turtle_edge = turtle.Turtle()
            turtle_edge.penup()
            turtle_edge.goto(x1 * 200, y1 * 200)
            turtle_edge.pendown()
            turtle_edge.width(3)
            turtle_edge.goto(x2 * 200, y2 * 200)
            self.edge_turtles[edge] = turtle_edge

    def draw_graph(self):
        for node, turtle_node in self.node_turtles.items():
            if node in self.visited_nodes:
                turtle_node.color('red')  # Change the color of visited nodes to red
                turtle_node.fillcolor('red')
                turtle_node.dot(20)  # Redraw the node
            else:
                turtle_node.color('skyblue')
                turtle_node.fillcolor('skyblue')

    def start_dfs(self):
        start_node = self.choose_start_node()
        if start_node:
            self.goal_node = self.choose_goal_node()  # Add prompt for goal node
            self.dfs(start_node)
            if self.goal_reached:
                messagebox.showinfo("DFS Completed", f"Goal node {self.goal_node} reached!\nDFS traversal path: {self.path}")
            else:
                messagebox.showinfo("DFS Completed", f"DFS traversal path: {self.path}")
            self.screen.bye()

    def dfs(self, node):
        self._dfs_recursive(node)

    def _dfs_recursive(self, node):
        self.visited_nodes.add(node)
        self.path.append(node)

        self.enqueue_count += 1  # Increment enqueue counter
        self.queue_size = len(self.path)  # Update queue size

        self.draw_graph()

        if node == self.goal_node:  # Stop the traversal if the goal node is reached
            self.goal_reached = True
            return

        for neighbor in self.graph.neighbors(node):
            if neighbor not in self.visited_nodes and not self.goal_reached:
                self.move_turtle(self.node_turtles[node], self.node_turtles[neighbor])
                while self.paused:
                    turtle.update()  # Wait for the space bar to be pressed
                self._dfs_recursive(neighbor)

    def move_turtle(self, start_turtle, end_turtle):
        if not isinstance(start_turtle, turtle.Turtle) or not isinstance(end_turtle, turtle.Turtle):
            return  # Skip moving if either turtle is not a valid Turtle instance

        start_turtle.speed(1)  # Adjust the speed (1 = slow, 10 = fast)
        start_turtle.penup()   # Lift the pen to hide the line
        start_turtle.goto(end_turtle.position())
        start_turtle.pendown()  # Lower the pen after moving
        start_turtle.penup()   # Lift the pen again to avoid drawing additional lines

    def toggle_pause(self):
        self.paused = not self.paused

    def choose_start_node(self):
        start_node_str = simpledialog.askstring("Input", "Enter the starting node:")
        try:
            start_node = int(start_node_str)
            if start_node in self.graph.nodes:
                return start_node
            else:
                messagebox.showwarning("Invalid Input", "Node not in the graph. Please enter a valid node.")
                return None
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid integer node.")
            return None

    def choose_goal_node(self):
        goal_node_str = simpledialog.askstring("Input", "Enter the goal node:")
        try:
            goal_node = int(goal_node_str)
            if goal_node in self.graph.nodes:
                return goal_node
            else:
                messagebox.showwarning("Invalid Input", "Goal node not in the graph. Please enter a valid node.")
                return None
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid integer node.")
            return None

# Example usage
if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (2, 9), (9, 7), (7, 9), (2, 3)])

    dfs_visualizer = DFSVisualizer(G)
    dfs_visualizer.draw_graph()
    dfs_visualizer.start_dfs()

    turtle.done()
