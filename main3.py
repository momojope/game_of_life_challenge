import random
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame

pygame.init()

# Couleur de base
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# var de base de la simulation
WIDTH, HEIGHT = 1520, 760
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 80
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# Slider et sa boite de texte pour la vitesse de sim
slider = Slider(screen, 40, 31, 250, 20, min=1, max=99, step=1)
output = TextBox(screen, 318, 29, 25, 25, fontSize=20)

# Slider et sa boite de texte le nbr de case généré aléatoirement
slider_Alea = Slider(screen, WIDTH - 59, 85, 39, 490, min=1, max=500, step=1, handleRadius=15, vertical=True)
output_Alea = TextBox(screen, WIDTH - 65, 10, 50, 50, fontSize=20)

# affiche le compteur de tours de sim
output_cmpt = TextBox(screen, (WIDTH // 2) - 40, 10, 85, 30, fontSize=20)

output.disable()  # Act as label instead of textbox
output_Alea.disable()


def gen(num):
    """Génère un set de position random"""
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])


def draw_hover(position):
    """Colorie la case survolée par le curseur"""
    col, row = position
    top_left = (col * TILE_SIZE, row * TILE_SIZE)
    pygame.draw.rect(screen, (180, 180, 80), (*top_left, TILE_SIZE, TILE_SIZE))


def draw_grid():
    """Dessine la grille et les cases 'vivante' """
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def draw_cases_vivante(positions, color):
    """Dessine les cases 'vivantes'"""
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, color, (*top_left, TILE_SIZE, TILE_SIZE))


def adjust_grid(positions):
    """Partie logique Update les cases vivantes"""
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))  # vérifie et renvoie si les voisins sont "vivant"

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    """Retourne les voisins d'une case"""
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))

    return neighbors


def main():
    """Lance le programme"""
    running = True
    playing = False
    count = 0  # égal au numéro de frame dans la seconde
    cmpt = 0  # égal au nbr de fois que la sim a été exécuter
    update_freq = 50  # Tick de la sim en fps

    # variables de contrôle clavier
    KEY_fleche_droite = False
    KEY_fleche_gauche = False

    # vars paramètres de sim
    chosen_color = YELLOW

    positions = set()  # set des positions (col, row) des cases vivantes

    while running:
        clock.tick(FPS)
        update_freq = 100 - (slider.getValue() % 100)  # plus la valeur est faible plus les rafraichissements son rapide

        if playing:
            count += 1

        if not playing:
            pygame.display.update()

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)
            cmpt += 1

        # met à jour le titre de la fenêtre
        pygame.display.set_caption("Playing" if playing else "Paused")

        events = pygame.event.get()
        # capture des évènements
        for event in events:

            # stop la boucle de jeu si event = quitter
            if event.type == pygame.QUIT:
                running = False

            # check si les touches sont pressé
            if event.type == pygame.KEYDOWN:
                # quite si 'echap' est cliqué
                if event.key == pygame.K_ESCAPE:
                    return pygame.quit()

                # joue et pause si 'espace' est cliqué
                if event.key == pygame.K_SPACE:
                    playing = not playing

                # clear la grille si 'C' est pressé
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                    cmpt = 0

                if event.key == pygame.K_g:
                    positions = gen(slider_Alea.getValue())

                if event.key == pygame.K_LEFT:
                    KEY_fleche_gauche = True
                    KEY_fleche_droite = False

                if event.key == pygame.K_RIGHT:
                    KEY_fleche_droite = True
                    KEY_fleche_gauche = False

                # incrémente la sim d'un tour sur clique de flèche haut
                if event.key == pygame.K_UP and not playing:
                    count = 0
                    positions = adjust_grid(positions)
                    cmpt += 1

            # check si les touches sont relever
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    KEY_fleche_gauche = False

                if event.key == pygame.K_RIGHT:
                    KEY_fleche_droite = False

        # change les vals du slider
        if KEY_fleche_gauche and (slider.getValue() > 1):
            slider.setValue((slider.getValue() - 0.5))

        if KEY_fleche_droite and slider.getValue() < 99:
            slider.setValue((slider.getValue() + 0.5))

        # récupère la pos du curseur quand la souris est cliqué
        # converti la pos en pixel en ligne et col de la grille
        mouse_presses = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        col = x // TILE_SIZE
        row = y // TILE_SIZE
        positionCursor = (col, row)

        # ajoute/retire une case vivante si elle n'est pas compris dans la zone des widgets
        if mouse_presses[0] and not ((y < 60) and (x < 330)) and not ((y < 600) and (x > 1450)):
            positions.add(positionCursor)

        elif mouse_presses[2]:
            if positionCursor in positions:
                positions.remove(positionCursor)

        # affichage de la grille et des cases
        screen.fill(GREY)
        draw_hover(positionCursor)
        draw_cases_vivante(positions, chosen_color)
        draw_grid()

        # lie event aux widgets pour interaction
        pygame_widgets.update(events)

        # affichage des widgets
        output.setText(round(slider.getValue()))
        output_Alea.setText("nb:" + str(slider_Alea.getValue()))
        output_cmpt.setText("count : " + str(cmpt))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()