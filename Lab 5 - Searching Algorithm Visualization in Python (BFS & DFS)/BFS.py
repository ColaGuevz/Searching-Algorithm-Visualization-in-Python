import networkx as nx
import turtle
from tkinter import messagebox, simpledialog
from collections import deque

class BFSVisualizer:
    def __init__(self, graph):
        self.graph = graph
        self.visited_nodes = set()
        self.path = []
        self.paused = False
        self.goal_node = None
        self.goal_reached = False
        self.enqueue_count = 0
        self.extension_count = 0
        self.queue_size = 0

        self.screen = turtle.Screen()
        self.screen.bgcolor("white")
        self.screen.title("BFS Visualizer")

        self.node_turtles = {}
        self.edge_turtles = {}
        self.create_turtles()

        self.screen.listen()
        self.screen.onkey(self.toggle_pause, "space")

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
                turtle_node.color('red')
                turtle_node.dot(20, 'red')
            else:
                turtle_node.color('skyblue')
                turtle_node.dot(20, 'skyblue')

        for edge, turtle_edge in self.edge_turtles.items():
            turtle_edge.hideturtle()

    def start_bfs(self):
        start_node = self.choose_start_node()
        if start_node:
            self.goal_node = self.choose_goal_node()
            self.bfs(start_node)
            if self.goal_reached:
                messagebox.showinfo("BFS Completed", f"Goal node {self.goal_node} reached!\nBFS traversal path: {self.path}")
            else:
                messagebox.showinfo("BFS Completed", f"BFS traversal path: {self.path}\nEnqueues: {self.enqueue_count}\nExtensions: {self.extension_count}\nQueue Size: {self.queue_size}")
            self.screen.bye()

    def bfs(self, start_node):
        queue = deque([start_node])
        self.visited_nodes.add(start_node)

        while queue:
            current_node = queue.popleft()
            self.path.append(current_node)

            self.draw_graph()

            if current_node == self.goal_node:  # Stop the traversal if the goal node is reached
                self.goal_reached = True
                return

            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in self.visited_nodes:
                    self.enqueue_count += 1
                    self.extension_count += 1
                    self.queue_size = len(queue)
                    self.move_turtle(self.node_turtles[current_node], self.node_turtles[neighbor])
                    while self.paused:
                        turtle.update()
                    queue.append(neighbor)
                    self.visited_nodes.add(neighbor)

    def move_turtle(self, start_turtle, end_turtle):
        if not isinstance(start_turtle, turtle.Turtle) or not isinstance(end_turtle, turtle.Turtle):
            return

        start_turtle.speed(1)
        start_turtle.penup()
        start_turtle.goto(end_turtle.position())
        start_turtle.pendown()
        start_turtle.penup()

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

    bfs_visualizer = BFSVisualizer(G)
    bfs_visualizer.draw_graph()
    bfs_visualizer.start_bfs()

    turtle.done()
