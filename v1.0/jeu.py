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
        self.premier_coup = {}
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
                             (self.selection[1] * 50, self.selection[2] * 50, 50, 50), 2)
        if self.coups_possibles:
            for i in self.coups_possibles:
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (i[1][0] * 50, i[1][1] * 50, 50, 50), 2)

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

    def cal_coup(self, indice, coord):
        deplacements, t = indice.deplacer(coord)
        boool = None
        coups = []
        if not deplacements:
            if t == "DAME":
                return self.dep_dame(indice, coord)
                # self.premier_coup[f"DAME {indice.get_coord()}"] = self.dep_dame(indice)
            elif t == "FOU":
                return self.dep_fou(indice, coord)
                # self.premier_coup[f"FOU {indice.get_coord()}"] = self.dep_fou(indice)
            elif t == "TOUR":
                return self.dep_tour(indice, coord)
                # self.premier_coup[f"TOUR {indice.get_coord()}"] = self.dep_tour(indice)
        else:
            if t == "PION":
                # ********************************************************** TODO : EN PASSANT !
                if deplacements[0] in self.cases_vides:
                    coups.append((None, deplacements[0]))
                if deplacements[1] not in self.cases_vides:
                    for pion in self.pions:
                        if pion.get_coord() == deplacements[1] and pion.get_color() != self.joueur:
                            coups.append((pion.type, deplacements[1]))
                if deplacements[2] not in self.cases_vides:
                    for pion in self.pions:
                        if pion.get_coord() == deplacements[2] and pion.get_color() != self.joueur:
                            coups.append((pion.type, deplacements[2]))
                if len(deplacements) == 4:
                    if deplacements[3] in self.cases_vides:
                        coups.append((None, deplacements[3]))
                return coups

            elif t == "CHEVAL" or t == "ROI":
                for case in deplacements:
                    for pion in self.pions:
                        if pion.get_coord() == case and pion.get_color() != self.joueur:
                            boool = pion.who()
                            break
                        else:
                            boool = None
                    if case in self.cases_vides or boool:
                        coups.append((boool, case))
                return coups

    def dep_fou(self, fou, coord):
        cases = []
        x, y = coord
        # En bas à droite
        for i in range(1, 8 - x):
            if (x + i, y + i) in self.cases_vides:
                cases.append((None, (x + i, y + i)))
            else:
                for pion in self.pions:
                    if (x + i, y + i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((pion.who(), (x + i, y + i)))
                        break
                    if (x + i, y + i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        # En bas à gauche
        for i in range(1, x + 1):
            if (x - i, y + i) in self.cases_vides:
                cases.append((None, (x - i, y + i)))
            else:
                for pion in self.pions:
                    if (x - i, y + i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((pion.who(), (x - i, y + i)))
                        break
                    if (x - i, y + i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        # En haut à droite
        for i in range(1, 8 - x):
            if (x + i, y - i) in self.cases_vides:
                cases.append((None, (x + i, y - i)))
            else:
                for pion in self.pions:
                    if (x + i, y - i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((pion.who(), (x + i, y - i)))
                        break
                    if (x + i, y - i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        # En haut à gauche
        for i in range(1, x + 1):
            if (x - i, y - i) in self.cases_vides:
                cases.append((None, (x - i, y - i)))
            else:
                for pion in self.pions:
                    if (x - i, y - i) == pion.get_coord() and pion.get_color() != fou.get_color():
                        cases.append((pion.who(), (x - i, y - i)))
                        break
                    if (x - i, y - i) == pion.get_coord() and pion.get_color() == fou.get_color():
                        break
                break
        return cases

    def dep_tour(self, tour, coord):
        cases = []
        x, y = coord
        # A droite
        for i in range(1, 8 - x):
            if (x + i, y) in self.cases_vides:
                cases.append((None, (x + i, y)))
            else:
                for pion in self.pions:
                    if (x + i, y) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((pion.who(), (x + i, y)))
                        break
                break
        # A gauche
        for i in range(1, x + 1):
            if (x - i, y) in self.cases_vides:
                cases.append((None, (x - i, y)))
            else:
                for pion in self.pions:
                    if (x - i, y) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((pion.who(), (x - i, y)))
                        break
                break
        # En bas
        for i in range(1, 8 - y):
            if (x, y + i) in self.cases_vides:
                cases.append((None, (x, y + i)))
            else:
                for pion in self.pions:
                    if (x, y + i) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((pion.who(), (x, y + i)))
                        break
                break
        # En haut
        for i in range(1, y + 1):
            if (x, y - i) in self.cases_vides:
                cases.append((None, (x, y - i)))
            else:
                for pion in self.pions:
                    if (x, y - i) == pion.get_coord() and pion.get_color() != tour.get_color():
                        cases.append((pion.who(), (x, y - i)))
                        break
                break
        return cases

    def dep_dame(self, dame, coord):
        cases = self.dep_fou(dame, coord) + self.dep_tour(dame, coord)
        return cases

    @staticmethod
    def mouse(mouse):
        mouse_x, mouse_y = mouse
        for y in range(8):
            for x in range(8):
                if x * 50 <= mouse_x < (x + 1) * 50 and y * 50 <= mouse_y < (y + 1) * 50:
                    return x, y

    def click(self, x, y):
        if not self.selection:
            for i in self.pions:
                if i.get_coord() == (x, y) and i.get_color() == self.joueur:
                    self.selection = (i.who(), x, y)
                    self.coups_possibles = self.premier_coup[f"{i.who()} {i.get_coord()}"]
                    print(self.coups_possibles)
                    print(self.rock)
                    break
        else:
            for i in range(len(self.coups_possibles)):
                if (x, y) == self.coups_possibles[i][1]:
                    return True, i
            if (x, y) in self.cases_vides:
                self.selection = None
                self.coups_possibles = None
                return False, None
            for i in self.pions:
                if i.get_coord() == (x, y) and i.get_color() == self.joueur:
                    self.selection = (i.who(), x, y)
                    self.coups_possibles = self.premier_coup[f"{i.who()} {i.get_coord()}"]
                    print(self.coups_possibles)
                    print(self.rock)
                    return False, None
        return False, None

    def changer_joueur(self):
        self.joueur, self.autre_joueur = self.autre_joueur, self.joueur

    def play(self, i):
        for pion in self.pions:
            if pion.get_coord() == (self.selection[1], self.selection[2]):
                pion.move(self.coups_possibles[i][1][0], self.coups_possibles[i][1][1])
                if self.coups_possibles[i][0]:
                    tour = None
                    if self.coups_possibles[i][0] == "P ROCK":
                        pion.move(self.coups_possibles[i][1][0], self.coups_possibles[i][1][1])
                        if pion.get_color():
                            tour = ((7, 7), (5, 7))
                        else:
                            tour = ((7, 0), (5, 0))
                    elif self.coups_possibles[i][0] == "G ROCK":
                        pion.move(self.coups_possibles[i][1][0], self.coups_possibles[i][1][1])
                        if pion.get_color():
                            tour = ((0, 7), (3, 7))
                        else:
                            tour = ((0, 0), (3, 0))
                    if tour:
                        for rock in self.pions:
                            if rock.get_coord() == tour[0]:
                                rock.move(tour[1][0], tour[1][1])
                    else:
                        for cible in self.pions:
                            if cible.get_coord() == self.coups_possibles[i][1] and cible.get_color() != self.joueur:
                                print("Mangé !")
                                self.pions.remove(cible)
                                break
                break
        self.selection = None
        self.coups_possibles = None

    def calculer_rock(self):  #                                                  Pas fini
        for indice in self.pions:
            self.premier_coup[f"{indice.type} {indice.get_coord()}"] = self.cal_coup(indice, indice.get_coord())

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

        for pion in self.pions:
            if pion.type == "ROI" and pion.already_moved:
                if pion.get_color():
                    self.rock[0] = [False, False]  # Blanc false
                else:
                    self.rock[1] = [False, False]  # Noir false

        if self.rock[1][0]:
            self.premier_coup["ROI (4, 0)"].append(("P ROCK", (6, 0)))
        if self.rock[1][1]:
            self.premier_coup["ROI (4, 0)"].append(("G ROCK", (2, 0)))
        if self.rock[0][0]:
            self.premier_coup["ROI (4, 7)"].append(("P ROCK", (6, 7)))
        if self.rock[0][1]:
            self.premier_coup["ROI (4, 7)"].append(("G ROCK", (2, 0)))

    def calculer_echec(self):  #                                  Pas fini
        # On prend les infos des rois
        dep_blanc = []
        dep_noir = []
        coord_blanc = ()
        coord_noir = ()
        # Filtre des déplacements du roi
        for i in self.pions:
            if i.type == "ROI":
                if i.get_color():
                    coord_blanc = i.get_coord()
                    for dep in self.premier_coup[f"ROI {coord_blanc}"]:
                        dep_blanc.append(dep[1])
                    dep_blanc = self.filtrer_cases_roi(dep_blanc, 1)
                    for dep in self.premier_coup[f"ROI {coord_blanc}"]:
                        if dep[1] not in dep_blanc:
                            self.premier_coup[f"ROI {coord_blanc}"].remove(dep)
                else:
                    coord_noir = i.get_coord()
                    for dep in self.premier_coup[f"ROI {coord_noir}"]:
                        dep_noir.append(dep[1])
                    dep_noir = self.filtrer_cases_roi(dep_noir, 0)
                    for dep in self.premier_coup[f"ROI {coord_noir}"]:
                        if dep[1] not in dep_noir:
                            self.premier_coup[f"ROI {coord_noir}"].remove(dep)

    def filtrer_cases_roi(self, dep_roi, color_roi):
        for pion in self.pions:
            for dep_pion in self.premier_coup[f"{pion.type} {pion.get_coord()}"]:
                if dep_pion[1] in dep_roi and pion.get_color() != color_roi:
                    dep_roi.remove(dep_pion[1])
        return dep_roi



    # On enlève les cases où le roi se mettrait en échec ET on regarde si le roi est en échec
    """for pion in self.pions:
        if pion.color:
            for dep in self.premier_coup[f"{pion.type} {pion.get_coord()}"]:
                for roi in dep_noir:
                    if dep[1] == roi[1]:
                        dep_noir.remove(roi)
                        break
                    if dep[1] == coord_noir:
                        print("Échec noir !")
                        for i in self.pions:
                            if i.type == "ROI" and not i.get_color():
                                i.check()
                                print("Validé")
                                break
                        break
        else:
            for dep in self.premier_coup[f"{pion.type} {pion.get_coord()}"]:
                for roi in dep_blanc:
                    if dep[1] == roi[1]:
                        dep_blanc.remove(roi)
                        break
                    if dep[1] == coord_blanc:
                        print("Échec blanc !")
                        for i in self.pions:
                            if i.type == "ROI" and i.get_color():
                                i.check()
                                print("Validé")
                                break
                        break"""
