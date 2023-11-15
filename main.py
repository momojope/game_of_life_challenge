import tkinter as tk
import random

class JeuDeLaVie:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(root, width=width*10, height=height*10, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        # Initialisation de la grille avec des cellules aléatoires
        self.grid = [[random.choice([0, 1]) for _ in range(width)] for _ in range(height)]

        # Boutons pour contrôler le jeu
        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_game)
        self.stop_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT)

        # Variable pour suivre l'état du jeu
        self.running = False

        # Mise à jour de l'affichage
        self.draw_grid()

    def start_game(self):
        self.running = True
        self.update()

    def stop_game(self):
        self.running = False

    def clear_grid(self):
        self.grid = [[0] * self.width for _ in range(self.height)]
        self.draw_grid()

    def update(self):
        if self.running:
            new_grid = [[0] * self.width for _ in range(self.height)]

            for i in range(self.width):
                for j in range(self.height):
                    neighbors = self.get_neighbors(i, j)
                    live_neighbors = sum(neighbors)

                    if self.grid[i][j] == 1:
                        if live_neighbors < 2 or live_neighbors > 3:
                            new_grid[i][j] = 0
                        else:
                            new_grid[i][j] = 1
                    else:
                        if live_neighbors == 3:
                            new_grid[i][j] = 1

            self.grid = new_grid
            self.draw_grid()
            self.root.after(100, self.update)

    def get_neighbors(self, x, y):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.width and 0 <= y + j < self.height:
                    neighbors.append(self.grid[x + i][y + j])
        return neighbors

    def draw_grid(self):
        self.canvas.delete("all")
        cell_size = 10

        for i in range(self.width):
            for j in range(self.height):
                x = i * cell_size
                y = j * cell_size
                if self.grid[i][j] == 1:
                    self.canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jeu de la Vie")
    jeu = JeuDeLaVie(root, 40, 40)
    root.mainloop()
