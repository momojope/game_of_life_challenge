import streamlit as st
import numpy as np
import time

class JeuDeLaVie:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_cellule = 15

        # Initialisation de la grille avec des cellules mortes
        self.grille = np.zeros((self.largeur, self.hauteur), dtype=int)

    def demarrer_jeu(self):
        """Démarrer le jeu en continuant la mise à jour automatique."""
        self.en_marche = True
        self.mettre_a_jour()

    def arreter_jeu(self):
        """Arrêter le jeu en interrompant la mise à jour automatique."""
        self.en_marche = False

    def effacer_grille(self):
        """Effacer la grille en remettant toutes les cellules à l'état mort."""
        self.grille = np.zeros((self.largeur, self.hauteur), dtype=int)
        self.dessiner_grille()

    def gerer_clic(self, coord):
        """Gérer le clic de la souris pour inverser l'état d'une cellule."""
        # Convertir les coordonnées du clic en indices de grille
        i, j = coord
        # Inverser l'état de la cellule
        self.grille[i, j] = 1 if self.grille[i, j] == 0 else 0
        self.dessiner_grille()

    def gerer_glisser(self, coord):
        """Gérer le déplacement de la souris pour activer les cellules."""
        # Activer la cellule
        i, j = coord
        self.grille[i, j] = 1
        self.dessiner_grille()

    def mettre_a_jour(self):
        """Mettre à jour la grille en suivant les règles du Jeu de la Vie."""
        while self.en_marche:
            nouvelle_grille = np.zeros((self.largeur, self.hauteur), dtype=int)

            for i in range(self.largeur):
                for j in range(self.hauteur):
                    voisins = self.obtenir_voisins(i, j)
                    voisins_vivants = sum(voisins)

                    if self.grille[i, j] == 1:
                        if voisins_vivants == 2 or voisins_vivants == 3:
                            nouvelle_grille[i, j] = 1
                    else:
                        if voisins_vivants == 3:
                            nouvelle_grille[i, j] = 1

            self.grille = nouvelle_grille
            self.dessiner_grille()
            time.sleep(0.1)

    def obtenir_voisins(self, x, y):
        """Obtenir les états des voisins d'une cellule."""
        voisins = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.largeur and 0 <= y + j < self.hauteur:
                    voisins.append(self.grille[x + i, y + j])
        return voisins

    def dessiner_grille(self):
        """Dessiner la grille."""
        st.image(self.grille, width=self.largeur * self.taille_cellule, clamp=True)

if __name__ == "__main__":
    st.title("Jeu de la Vie de John Conway")

    largeur, hauteur = st.slider("Choisir la taille de la grille", 5, 50, (20, 20), step=1)
    jeu = JeuDeLaVie(largeur, hauteur)

    st.button("Démarrer", on_click=jeu.demarrer_jeu)
    st.button("Arrêter", on_click=jeu.arreter_jeu)
    st.button("Effacer", on_click=jeu.effacer_grille)

    st.image(np.zeros((largeur, hauteur), dtype=int), width=largeur * jeu.taille_cellule, clamp=True, key="empty_grid")

    grid_chart = st.image(np.zeros((largeur, hauteur), dtype=int), width=largeur * jeu.taille_cellule, clamp=True, key="grid")
    grid_chart.click_callback(jeu.gerer_clic)
    grid_chart.drag_callback(jeu.gerer_glisser)
