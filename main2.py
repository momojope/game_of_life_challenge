import tkinter as tk
import random

class JeuDeLaVie:
    def __init__(self, root, width, height):
        self.root = root
        self.width = width
        self.height = height
        self.cell_size = 15

        # Initialisation de la grille avec des cellules mortes
        self.grid = [[0] * self.width for _ in range(self.height)]

        # Créer le canevas
        self.canvas = tk.Canvas(root, width=width * self.cell_size, height=height * self.cell_size, borderwidth=1,
                                highlightthickness=0, bg="white")
        self.canvas.pack()

        # Ajouter la grille en arrière-plan
        self.draw_background_grid()

        # Boutons pour contrôler le jeu
        self.start_button = tk.Button(root, text="Start", command=self.start_game, padx=10, bg="#4CAF50", fg="white")
        self.start_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_game, padx=10, bg="#f44336", fg="white")
        self.stop_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_grid, padx=10, bg="#2196F3", fg="white")
        self.clear_button.pack(side=tk.LEFT)

        # Variable pour suivre l'état du jeu
        self.running = False

        # Ajouter la gestion des clics
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)

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

    def handle_click(self, event):
        # Convertir les coordonnées du clic en indices de grille
        i, j = event.x // self.cell_size, event.y // self.cell_size
        # Inverser l'état de la cellule
        self.grid[i][j] = 1 if self.grid[i][j] == 0 else 0
        self.draw_grid()

    def handle_drag(self, event):
        # Convertir les coordonnées du mouvement en indices de grille
        i, j = event.x // self.cell_size, event.y // self.cell_size
        # Activer la cellule
        self.grid[i][j] = 1
        self.draw_grid()

    def update(self):
        if self.running:
            new_grid = [[0] * self.width for _ in range(self.height)]

            for i in range(self.width):
                for j in range(self.height):
                    neighbors = self.get_neighbors(i, j)
                    live_neighbors = sum(neighbors)

                    if self.grid[i][j] == 1:
                        if live_neighbors == 2 or live_neighbors == 3:
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
        self.canvas.delete("cells")

        for i in range(self.width):
            for j in range(self.height):
                x = i * self.cell_size
                y = j * self.cell_size
                if self.grid[i][j] == 1:
                    self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                                 fill="black", outline="gray", tags="cells")

    def draw_background_grid(self):
        for i in range(self.width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.height * self.cell_size, fill="gray", tags="grid")

        for j in range(self.height + 1):
            y = j * self.cell_size
            self.canvas.create_line(0, y, self.width * self.cell_size, y, fill="gray", tags="grid")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Challenge Elias  / Jeu de la Vie de John Conway")
    jeu = JeuDeLaVie(root, 40, 40)
    root.mainloop()
