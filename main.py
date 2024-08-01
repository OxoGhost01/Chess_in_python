import pygame
import sys
import jeu

from pygame.locals import *

"""
Pions :
1 = BLANC
0 = NOIR
 
Rock :
1 = grand
0 = petit
"""

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Chess.com")
clock = pygame.time.Clock()
sysFont = pygame.font.SysFont("None", 32)
beige = (253, 235, 208)
plateau = jeu.Plateau(screen)
plateau.cree_plateau()
while True:
    screen.fill(beige)
    plateau.affiche_plateau()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not plateau.selection:
                plateau.update_cases_vides()
                plateau.calculer_rock()
                # plateau.calculer_echec()
            mx, my = plateau.mouse(pygame.mouse.get_pos())
            indice_coup = plateau.click(mx, my)
            if indice_coup is not None:
                plateau.play(indice_coup)
                plateau.changer_joueur()
        if event.type == QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    pygame.display.update()
