import pygame.draw

from pion import *


class Plateau:
    def __init__(self, screen):
        """
        Pour améliorer : faire fonction de recherche de pion commune
                         stocker les déplacements des pions directement dans leurs paramètres
        """
        self.pions = []
        self.cases_vides = []
        self.screen = screen
        self.selection = None
        self.coups_possibles = []
        self.joueur = 1
        self.autre_joueur = 0
        self.rock = [[False, False], [False, False]]
        # self.rock = [[True, True], [True, True]]

    def affiche_plateau(self):
        # Cases
        boool = True  # True = case verte au début de la ligne
        for y in range(8):
            boool = False if boool else True
            if boool:
                for x in range(0, 8, 2):
                    pygame.draw.rect(self.screen, (50, 150, 50), (x * 50, y * 50, 50, 50))
            else:
                for x in range(1, 9, 2):
                    pygame.draw.rect(self.screen, (50, 150, 50), (x * 50, y * 50, 50, 50))

        for case in self.pions:
            case.draw()

        if self.selection:
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (self.pions[self.selection].get_coord()[0] * 50,
                              self.pions[self.selection].get_coord()[1] * 50, 50, 50), 2)
        if self.coups_possibles:
            for i in self.coups_possibles:
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (i[0] * 50, i[1] * 50, 50, 50), 2)

    def update_cases_vides(self):
        self.cases_vides = []
        for y in range(8):
            for x in range(8):
                boool = False
                for i in self.pions:
                    if (x, y) == i.get_coord():
                        boool = True
                        break
                if not boool:
                    self.cases_vides.append((x, y))

    def cree_plateau(self):
        # Création des pions
        for x in range(8):
            self.pions.append(Pion(x, 1, 0, self.screen, "PION"))
            self.pions.append(Pion(x, 6, 1, self.screen, "PION"))

        # Création des pions spéciaux
        pions = ["TOUR", "CHEVAL", "FOU", "DAME"]
        for x in range(4):
            self.pions.append(Pion(x, 0, 0, self.screen, pions[x], 1))
            self.pions.append(Pion(x, 7, 1, self.screen, pions[x], 1))
        for x in range(3):
            self.pions.append(Pion(5 + x, 0, 0, self.screen, pions[2 - x], 0))
            self.pions.append(Pion(5 + x, 7, 1, self.screen, pions[2 - x], 0))

        # Création des rois
        self.pions.append(Pion(4, 7, 1, self.screen, "ROI"))
        self.pions.append(Pion(4, 0, 0, self.screen, "ROI"))

        # Création des cases vides

        for y in range(2, 6):
            for x in range(8):
                self.cases_vides.append((x, y))

    def chercher_pion(self, coord):
        n, i = len(self.pions), 0
        while i < n:
            if self.pions[i].get_coord() == coord:
                return i
            i += 1
        return None
                    
    def cal_coup(self, pion, coord):
        deplacements, t = pion.deplacer(coord)
        boool = None
        coups = []
        mange = []
        if not deplacements:
            if t == "DAME":
                return self.dep_dame(pion, coord)
            elif t == "FOU":
                return self.dep_fou(pion, coord)
            elif t == "TOUR":
                return self.dep_tour(pion, coord)
        else:
            if t == "PION":
                # ********************************************************** TODO : EN PASSANT !
                if deplacements[0] in self.cases_vides:
                    coups.append(deplacements[0])
                    mange.append(False)
                if deplacements[1] not in self.cases_vides:
                    for pion in self.pions:
                        if pion.get_coord() == deplacements[1] and pion.get_color() != self.joueur:
                            coups.append(deplacements[1])
                            mange.append(True)
                if deplacements[2] not in self.cases_vides:
                    for pion in self.pions:
                        if pion.get_coord() == deplacements[2] and pion.get_color() != self.joueur:
                            coups.append(deplacements[2])
                            mange.append(True)
                if len(deplacements) == 4:
                    if deplacements[3] in self.cases_vides:
                        coups.append(deplacements[3])
                        mange.append(False)
                return coups, mange

            elif t == "CHEVAL" or t == "ROI":
                for case in deplacements:
                    for pion in self.pions:
                        if pion.get_coord() == case and pion.get_color() != self.joueur:
                            boool = True
                            break
                        else:
                            boool = False
                    if case in self.cases_vides or boool:
                        coups.append(case)
                        mange.append(boool)
                return coups, mange

    def dep_fou(self, fou, coord):
        cases = []
        mange = []
        x, y = coord
        # En bas à droite
        for i in range(1, 8 - x):
            if (x + i, y + i) in self.cases_vides:
                cases.append((x + i, y + i))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x + i, y + i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((x + i, y + i))
                        mange.append(True)
                        break
                    if (x + i, y + i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        # En bas à gauche
        for i in range(1, x + 1):
            if (x - i, y + i) in self.cases_vides:
                cases.append((x - i, y + i))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x - i, y + i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((x - i, y + i))
                        mange.append(True)
                        break
                    if (x - i, y + i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        # En haut à droite
        for i in range(1, 8 - x):
            if (x + i, y - i) in self.cases_vides:
                cases.append((x + i, y - i))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x + i, y - i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((x + i, y - i))
                        mange.append(True)
                        break
                    if (x + i, y - i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        # En haut à gauche
        for i in range(1, x + 1):
            if (x - i, y - i) in self.cases_vides:
                cases.append((x - i, y - i))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x - i, y - i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((x - i, y - i))
                        mange.append(True)
                        break
                    if (x - i, y - i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        return cases, mange

    def dep_tour(self, tour, coord):
        cases = []
        mange = []
        x, y = coord
        # A droite
        for i in range(1, 8 - x):
            if (x + i, y) in self.cases_vides:
                cases.append((x + i, y))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x + i, y) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((x + i, y))
                        mange.append(True)
                        break
                break
        # A gauche
        for i in range(1, x + 1):
            if (x - i, y) in self.cases_vides:
                cases.append((x - i, y))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x - i, y) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((x - i, y))
                        mange.append(True)
                        break
                break
        # En bas
        for i in range(1, 8 - y):
            if (x, y + i) in self.cases_vides:
                cases.append((x, y + i))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x, y + i) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((x, y + i))
                        mange.append(True)
                        break
                break
        # En haut
        for i in range(1, y + 1):
            if (x, y - i) in self.cases_vides:
                cases.append((x, y - i))
                mange.append(False)
            else:
                for pion in self.pions:
                    if (x, y - i) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((x, y - i))
                        mange.append(True)
                        break
                break
        return cases, mange

    def dep_dame(self, dame, coord):
        cases_fou = self.dep_fou(dame, coord)
        cases_tour = self.dep_tour(dame, coord)
        coups = cases_fou[0] + cases_tour[0]
        mange = cases_fou[1] + cases_tour[1]
        return coups, mange

    @staticmethod
    def mouse(mouse):
        mouse_x, mouse_y = mouse
        for y in range(8):
            for x in range(8):
                if x * 50 <= mouse_x < (x + 1) * 50 and y * 50 <= mouse_y < (y + 1) * 50:
                    return x, y

    def click(self, x, y):
        if not self.selection:
            for indice in range(len(self.pions)):
                if self.pions[indice].get_coord() == (x, y) and self.pions[indice].get_color() == self.joueur:
                    self.selection = indice  # TODO: J'ai changé ca !!!
                    self.coups_possibles = self.pions[indice].coup1
                    print(self.coups_possibles)
                    print(self.rock)
                    return None
        else:
            for i_coup in range(len(self.coups_possibles)):
                if (x, y) == self.coups_possibles[i_coup]:
                    return i_coup
            if (x, y) in self.cases_vides:
                self.selection = None
                self.coups_possibles = None
                return None
            for indice in range(len(self.pions)):
                if self.pions[indice].get_coord() == (x, y) and self.pions[indice].get_color() == self.joueur:
                    self.selection = indice
                    self.coups_possibles = self.pions[indice].coup1
                    print(self.coups_possibles)
                    print(self.rock)
                    return None

    def changer_joueur(self):
        self.joueur, self.autre_joueur = self.autre_joueur, self.joueur

    def play(self, indice_coup):
        pion = self.pions[self.selection]
        tour = None
        if pion.mange1[indice_coup]:
            if pion.mange1[indice_coup] == "PR":
                if pion.get_color():
                    tour = ((7, 7), (5, 7))
                else:
                    tour = ((7, 0), (5, 0))
            elif pion.mange1[indice_coup] == "GR":
                if pion.get_color():
                    tour = ((0, 7), (3, 7))
                else:
                    tour = ((0, 0), (3, 0))
            else:
                print("Mangé !")
                self.pions.remove(self.pions[self.chercher_pion(pion.coup1[indice_coup])])
        if tour:
            self.pions[self.chercher_pion(tour[0])].move(tour[1])
        pion.move(pion.coup1[indice_coup])
        self.selection = None
        self.coups_possibles = None

    def calculer_rock(self):
        for pion in self.pions:
            pion.coup1, pion.mange1 = self.cal_coup(pion, pion.get_coord())

        # Noirs
        # Petit Rock
        if (5, 0) in self.cases_vides and (6, 0) in self.cases_vides:
            self.rock[1][0] = True
        # Grand Rock
        if (1, 0) in self.cases_vides and (2, 0) in self.cases_vides and (3, 0) in self.cases_vides:
            self.rock[1][1] = True
        # Blancs
        # Petit Rock
        if (5, 7) in self.cases_vides and (6, 7) in self.cases_vides:
            self.rock[0][0] = True
            print("Petit blanc", self.rock)
        # Grand Rock
        if (1, 7) in self.cases_vides and (2, 7) in self.cases_vides and (3, 7) in self.cases_vides:
            self.rock[0][1] = True

        # Appel du calcul des échecs pour savoir si le roi peut rocker
        self.calculer_echec()

        for pion in self.pions:
            if pion.type == "ROI" and pion.already_moved:
                if pion.get_color():
                    self.rock[0] = [False, False]  # Blanc false
                else:
                    self.rock[1] = [False, False]  # Noir false

        if self.rock[1][0]:
            self.pions[self.chercher_pion((4, 0))].coup1.append((6, 0))
            self.pions[self.chercher_pion((4, 0))].mange1.append("PR")
        if self.rock[1][1]:
            self.pions[self.chercher_pion((4, 0))].coup1.append((2, 0))
            self.pions[self.chercher_pion((4, 0))].mange1.append("GR")
        if self.rock[0][0]:
            self.pions[self.chercher_pion((4, 7))].coup1.append((6, 7))
            self.pions[self.chercher_pion((4, 7))].mange1.append("PR")
        if self.rock[0][1]:
            self.pions[self.chercher_pion((4, 7))].coup1.append((2, 7))
            self.pions[self.chercher_pion((4, 7))].mange1.append("GR")

    def calculer_echec(self):                                       # Pas fini
        indices = []
        for i in range(len(self.pions)):
            if self.pions[i].type == "ROI":
                self.filtrer_cases_roi(i, self.pions[i].coup1, self.pions[i].get_coord())
                indices.append(i)
        """for i in indices:
            roi = self.pions[i]
            if roi.checky:
                self.oh_shit()"""

    def filtrer_cases_roi(self, indice, coups_roi, coord):
        for pion in self.pions:
            if pion.get_color() != self.pions[indice].get_color():
                for dep in pion.coup1:
                    if dep in coups_roi:
                        coups_roi.remove(dep)
                    if dep == coord:
                        self.pions[indice].check()
                        print("Echec !")

    def oh_shit(self):
        ...
