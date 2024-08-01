import pygame


class Pion:
    def __init__(self, x, y, color, screen, type, cote=None):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = color
        self.type = type
        self.already_moved = False
        self.checky = False
        self.cote = cote  # 1 = grand, 0 = petit (rock)
        self.coup1 = []
        self.mange1 = []  # False = pas de pion à manger ; True = pion à manger ; "PR" = petit rock ; "GR" = grand rock

    def check(self):
        self.checky = True if not self.checky else False

    def get_coord(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def move(self, coord):
        self.x, self.y = coord
        if not self.already_moved:
            self.already_moved = True

    def draw(self):
        # Initialisation de toutes les images

        pion_noir = pygame.image.load("img/pion_noir.png")
        pion_blanc = pygame.image.load("img/pion_blanc.png")
        dame_noire = pygame.image.load("img/dame_noir.png")
        dame_blanche = pygame.image.load("img/dame_blanc.png")
        roi_noir = pygame.image.load("img/roi_noir.png")
        roi_blanc = pygame.image.load("img/roi_blanc.png")
        tour_noire = pygame.image.load("img/tour_noir.png")
        tour_blanche = pygame.image.load("img/tour_blanc.png")
        fou_noir = pygame.image.load("img/fou_noir.png")
        fou_blanc = pygame.image.load("img/fou_blanc.png")
        cheval_noir = pygame.image.load("img/cavalier_noir.png")
        cheval_blanc = pygame.image.load("img/cavalier_blanc.png")

        # Dessin

        if self.color:
            if self.type == "PION":
                self.screen.blit(pion_blanc, (self.x * 50, self.y * 50))
            elif self.type == "TOUR":
                self.screen.blit(tour_blanche, (self.x * 50, self.y * 50))
            elif self.type == "CHEVAL":
                self.screen.blit(cheval_blanc, (self.x * 50, self.y * 50))
            elif self.type == "FOU":
                self.screen.blit(fou_blanc, (self.x * 50, self.y * 50))
            elif self.type == "DAME":
                self.screen.blit(dame_blanche, (self.x * 50, self.y * 50))
            elif self.type == "ROI":
                self.screen.blit(roi_blanc, (self.x * 50, self.y * 50))
        else:
            if self.type == "PION":
                self.screen.blit(pion_noir, (self.x * 50, self.y * 50))
            elif self.type == "TOUR":
                self.screen.blit(tour_noire, (self.x * 50, self.y * 50))
            elif self.type == "CHEVAL":
                self.screen.blit(cheval_noir, (self.x * 50, self.y * 50))
            elif self.type == "FOU":
                self.screen.blit(fou_noir, (self.x * 50, self.y * 50))
            elif self.type == "DAME":
                self.screen.blit(dame_noire, (self.x * 50, self.y * 50))
            elif self.type == "ROI":
                self.screen.blit(roi_noir, (self.x * 50, self.y * 50))

    def deplacer(self, coord):
        deplacements = []
        x, y = coord
        if self.type == "ROI":
            roi = [(-1, -1), (0, -1), (1, -1), (1, 0), (-1, 0), (-1, 1), (0, 1), (1, 1)]
            for i in roi:
                deplacements.append((x + i[0], y + i[1]))
        elif self.type == "PION":
            pion_blanc = [(0, 1), (1, 1), (-1, 1)]
            pion_noir = [(0, -1), (-1, -1), (1, -1)]
            if self.color:
                for i in pion_blanc:
                    deplacements.append((x + i[0], y - i[1]))
                if not self.already_moved:
                    deplacements.append((x, y - 2))
            else:
                for i in pion_noir:
                    deplacements.append((x + i[0], y - i[1]))
                if not self.already_moved:
                    deplacements.append((x, y + 2))
        elif self.type == "CHEVAL":
            # Haut, droite, bas, gauche
            cheval = [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)]
            for i in cheval:
                deplacements.append((x + i[0], y + i[1]))
        return deplacements, self.type
