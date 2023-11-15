import tkinter as tk
from tkinter import font

class JeuDeLaVie:
    def __init__(self, root, largeur, hauteur):
        self.root = root
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_cellule = 15
        self.compteur_cellules_vivantes = 0
        self.delai_mise_a_jour = 100 
        
        

        #ajout d'' un titre texte
        titre_font = font.Font(size=16, weight='bold')
        titre_label = tk.Label(root, text="CHALLENGE ELIAS, Jeu de la Vie de John Conway", font=titre_font)
        titre_label.pack(side=tk.TOP, pady=10)

        #initialisation de la grille avec des cellules mortes
        self.grille = [[0] * self.largeur for _ in range(self.hauteur)]

        #creation du canva 
        self.canevas = tk.Canvas(root, width=self.largeur * self.taille_cellule, height=self.hauteur * self.taille_cellule, borderwidth=1,
                                highlightthickness=0, bg="grey") 
        self.canevas.pack()
        self.dessiner_grille_arriere_plan()

        #liste des btn de jeu
        button_font = font.Font(size=12, weight='bold')
        self.bouton_demarrer = tk.Button(root, text="Démarrer", command=self.toggle_jeu, padx=15, pady=10, bg="#28a745", fg="white", relief=tk.FLAT, font=button_font)
        self.bouton_demarrer.pack(side=tk.LEFT, padx=5, pady=5)

        self.bouton_arreter = tk.Button(root, text="Arrêter", command=self.toggle_jeu, padx=15, pady=10, bg="#dc3545", fg="white", relief=tk.FLAT, font=button_font)
        self.bouton_arreter.pack(side=tk.LEFT, padx=5, pady=5)

        self.bouton_effacer = tk.Button(root, text="Effacer", command=self.effacer_grille, padx=15, pady=10, bg="#007bff", fg="white", relief=tk.FLAT, font=button_font)
        self.bouton_effacer.pack(side=tk.LEFT, padx=5, pady=5)

        #affichage compteur de cellules vivantes
        label_font = font.Font(size=14, weight='bold')
        self.label_compteur_cellules_vivantes = tk.Label(root, text="Cellules vivantes: 0", font=label_font)
        self.label_compteur_cellules_vivantes.pack(pady=5)

        #regulation de la vitesse de generation
        self.slider_vitesse = tk.Scale(root, from_=10, to=500, orient=tk.HORIZONTAL, label="Vitesse (ms)",
                                       length=200, command=self.mettre_a_jour_vitesse)
        self.slider_vitesse.set(self.delai_mise_a_jour)
        self.slider_vitesse.pack(pady=5)

        #variable pour check l'etat du jeu
        self.en_marche = False

        #event click
        self.canevas.bind("<Button-1>", self.gerer_clic)
        self.canevas.bind("<B1-Motion>", self.gerer_glisser)

        #ges curseur
        self.canevas.bind("<Enter>", self.changer_couleur_curseur)
        self.canevas.bind("<Leave>", self.restaurer_couleur_curseur)

        #generation
        self.dessiner_grille()
        
        
        
        

    def toggle_jeu(self):
        """Basculer entre le demarrage et l'arret du jeu"""
        self.en_marche = not self.en_marche
        self.bouton_demarrer["state"] = "disabled" if self.en_marche else "normal"
        self.bouton_arreter["state"] = "disabled" if not self.en_marche else "normal"
        if self.en_marche:
            self.mettre_a_jour()

    def demarrer_jeu(self):
        """demarrage du jeu en continuant la mise à jour automatique."""
        self.en_marche = True
        self.mettre_a_jour()

    def arreter_jeu(self):
        """arret du jeu en interrompant la mise à jour automatique"""
        self.en_marche = False

    def effacer_grille(self):
        """effacer la grille en remettant toutes   les cellules à l'etat dead"""
        self.grille = [[0] * self.largeur for _ in range(self.hauteur)]
        self.dessiner_grille()
        
        
        
        
        
        

    def gerer_clic(self, event):
        """Gestion du clic de la souris pour inverser l'état d'une cellule"""
        #convertir les coordonnees du clic en indices de grille
        i, j = event.x // self.taille_cellule, event.y // self.taille_cellule
        #inverseement de l'état de la cellule
        self.grille[i][j] = 1 if self.grille[i][j] == 0 else 0
        self.dessiner_grille()

        #mise à jour du compteur de cellules vivantes
        self.compteur_cellules_vivantes = sum([sum(row) for row in self.grille])
        self.label_compteur_cellules_vivantes.config(text="Cellules vivantes: {}".format(self.compteur_cellules_vivantes))

    def gerer_glisser(self, event):
        """gestion du deplacement de la souris pour activer les cellules."""
        #convertion des coordonnées du mouvement en indices de grille
        i, j = event.x // self.taille_cellule, event.y // self.taille_cellule
        #activation de la cellule
        self.grille[i][j] = 1
        self.dessiner_grille()

        #mise à jour du compteur de cellules vivantes
        self.compteur_cellules_vivantes = sum([sum(row) for row in self.grille])
        self.label_compteur_cellules_vivantes.config(text="Cellules vivantes: {}".format(self.compteur_cellules_vivantes))
        
        
        
        

    def mettre_a_jour(self):
        """mise a jourde la grille en suivant les règles du Jeu"""
        if self.en_marche:
            nouvelle_grille = [[0] * self.largeur for _ in range(self.hauteur)]

            for i in range(self.largeur):
                for j in range(self.hauteur):
                    voisins = self.obtenir_voisins(i, j)
                    voisins_vivants = sum(voisins)

                    if self.grille[i][j] == 1:
                        if voisins_vivants == 2 or voisins_vivants == 3:
                            nouvelle_grille[i][j] = 1
                    else:
                        if voisins_vivants == 3:
                            nouvelle_grille[i][j] = 1

            self.grille = nouvelle_grille
            self.dessiner_grille()

            #mettre a jour du compteur de cellules vivantes
            self.compteur_cellules_vivantes = sum([sum(row) for row in self.grille])
            self.label_compteur_cellules_vivantes.config(text="Cellules vivantes: {}".format(self.compteur_cellules_vivantes))

            self.root.after(self.delai_mise_a_jour, self.mettre_a_jour)

    def obtenir_voisins(self, x, y):
        """obtenir les états des voisins d'une cellule."""
        voisins = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.largeur and 0 <= y + j < self.hauteur:
                    voisins.append(self.grille[x + i][y + j])
        return voisins

    def dessiner_grille(self):
        """dessiner la grille avec des rectangles représentant les cellules."""
        self.canevas.delete("cellules")

        for i in range(self.largeur):
            for j in range(self.hauteur):
                x = i * self.taille_cellule
                y = j * self.taille_cellule
                if self.grille[i][j] == 1:
                    self.canevas.create_rectangle(x, y, x + self.taille_cellule, y + self.taille_cellule,
                                                  fill="#343a40", outline="yellow", tags="cellules", width=2)
                    
                    
                    

    def dessiner_grille_arriere_plan(self):
        """dessiner la grille en arrière-plan."""
        for i in range(self.largeur + 1):
            x = i * self.taille_cellule
            self.canevas.create_line(x, 0, x, self.hauteur * self.taille_cellule, fill="black", tags="grille", width=1)

        for j in range(self.hauteur + 1):
            y = j * self.taille_cellule
            self.canevas.create_line(0, y, self.largeur * self.taille_cellule, y, fill="black", tags="grille", width=1)

    def changer_couleur_curseur(self, event):
        """changer la couleur du curseur lorsqu'il survole le canevas."""
        self.canevas.config(cursor="plus")

    def restaurer_couleur_curseur(self, event):
        """restaurer la couleur du curseur lorsque le curseur quitte le canevas."""
        self.canevas.config(cursor="")

    def mettre_a_jour_vitesse(self, valeur):
        """mise a jour de la vitesse en fonction de la position du slider."""
        self.delai_mise_a_jour = int(valeur)

if __name__ == "__main__":
    racine = tk.Tk()
    racine.title("Jeu de la Vie de John Conway / Mohamed diop (@medmining)")
    jeu = JeuDeLaVie(racine, 40, 40 )

    #Ajout des lignes pour ajuster la taille de la fenêtre
    largeur_ecran = racine.winfo_screenwidth()
    hauteur_ecran = racine.winfo_screenheight()
    racine.geometry(f"{largeur_ecran}x{hauteur_ecran}+0+0")
    

    racine.mainloop()
