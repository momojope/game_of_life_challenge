# Jeu de la Vie de John Conway

![jeu](https://github.com/momojope/game_of_life_challenge/assets/61116986/6100c384-32e9-42ae-a181-727d2d3e73c6) ![jeu2](https://github.com/momojope/game_of_life_challenge/assets/61116986/ac5cf553-bfcb-4e83-9d93-3d61b5516d46)

## Auteurs

Mohamed diop @med_mining- Data & soft ing

## Description

Ce projet implémente le "Jeu de la Vie" de John Conway en utilisant Python et l'interface graphique Tkinter. Le Jeu de la Vie est un automate cellulaire bidimensionnel où l'évolution des cellules est déterminée par des règles simples basées sur l'état de leurs voisines.

## Fonctionnalités

- **Interface Graphique :** L'application utilise Tkinter pour créer une interface graphique conviviale.
- **Interaction Utilisateur :** Les utilisateurs peuvent cliquer sur les cellules pour les activer ou les désactiver. Le glissement de la souris permet également d'activer plusieurs cellules.
- **Contrôles du Jeu :** Les boutons "Démarrer", "Arrêter" et "Effacer" permettent de contrôler le jeu. Un slider ajuste la vitesse de mise à jour.
- **Affichage Dynamique :** L'interface graphique est mise à jour en temps réel pour refléter l'évolution de la grille.
- **Récursivité :** La mise à jour du jeu est gérée de manière récursive pour créer une boucle périodique.


## Commentaires Codage

# 1. Initialisation de la Grille :
    - La grille du jeu est une liste bidimensionnelle (matrice) initialisée avec des cellules mortes.

# 2. Gestion des Boutons d'Interaction :
    - Les boutons "Démarrer", "Arrêter", et "Effacer" sont associés à des méthodes pour contrôler le jeu.
    - Le bouton "Démarrer" bascule entre le démarrage et l'arrêt du jeu.

# 3. Gestion des Clics et Mouvements de Souris :
    - Les événements de clic et de mouvement de souris sont gérés pour activer et désactiver les cellules.
    - Les méthodes gerer_clic et gerer_glisser sont appelées en réponse à ces événements.

# 4. Mise à Jour Continue du Jeu :
    - La méthode mettre_a_jour utilise les règles du Jeu de la Vie pour mettre à jour la grille de manière continue.
    - Utilisation de la récursivité avec after de Tkinter pour des mises à jour périodiques.

# 5. Calcul des Voisins :
    - La méthode obtenir_voisins calcule l'état des huit voisins d'une cellule.
    - Utilisation d'une double boucle pour explorer les voisins autour de la cellule actuelle.


# 8. Gestion de la Vitesse de Génération :
    - Le slider_vitesse est utilisé pour réguler la vitesse de génération du jeu.
    - La méthode mettre_a_jour_vitesse ajuste la vitesse en fonction de la position du slider.


 # 9. Organisation Orientée Objet :
   - La classe JeuDeLaVie est utilisée pour encapsuler le jeu et ses fonctionnalités.
   - Les méthodes sont regroupées de manière logique, ce qui améliore la lisibilité et la maintenance du code.

# 10. Utilisation de Tkinter pour l'Interface Graphique :
   - Tkinter est choisi pour sa simplicité et sa présence standard dans les installations Python.
   - Les widgets Tkinter sont utilisés pour créer une interface utilisateur interactive.
# 11. Mise à Jour Automatique
    -La mise à jour du jeu est gérée de manière récursive à l'aide de la méthode `after` de Tkinter, créant ainsi une boucle périodique pour la génération continue.

# 12. Gestion des Événements de Souris :
   - La classe JeuDeLaVie réagit aux clics et mouvements de souris pour interagir avec la grille du jeu.

# 13. Utilisation de Tags dans le Canevas :
   - Des tags "cellules" et "grille" sont utilisés pour identifier les objets sur le canevas.
   - Facilite la gestion et la suppression des éléments graphiques.

# 14. Délai entre les Mises à Jour :
   - Utilisation de la méthode `after` de Tkinter pour planifier des mises à jour périodiques du jeu.
   - La vitesse de mise à jour est réglable via un slider.
# 15. Utilisation d'une Liste de Compréhension :
   - Des listes de compréhension sont utilisées pour initialiser la grille et calculer le nombre de cellules vivantes.

# 16. Personnalisation du Curseur :
   - Le curseur de la souris est modifié lorsqu'il survole le canevas pour une expérience utilisateur améliorée.

# 17. Ajout de Commentaires Détaillés dans Chaque Méthode :
   - Chaque méthode est commentée pour expliquer son rôle et son fonctionnement.
  
## run

Assurez-vous d'avoir Python installé sur votre machine.
Clonez ce dépôt : `git clone https://github.com/momojope/game_of_life_challenge.git`
Exécutez le programme : `python challenge_jdlv.py`

## extrait de l'interface

![Jeu de la Vie de John Conway _ Mohamed diop (@medmining) 15_11_2023 16_26_22](https://github.com/momojope/game_of_life_challenge/assets/61116986/92bdd18c-f45a-41e3-b32b-66a618d1ad10)
