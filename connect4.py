import numpy as np
import pygame
import sys
import math

#velikost mreze
st_vrstic = 6
st_stolpcev = 7

#rgb barve
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
PINK = (230, 25, 97)
GREEN = (57, 255, 20)


def ustvari_mrezo():
    mreza = np.zeros((st_vrstic, st_stolpcev))
    return mreza


def igraj(mreza, vrstica, stolpec, barva):
    mreza[vrstica][stolpec] = barva


def veljavna_poteza(mreza, stolpec):
    return mreza[st_vrstic - 1][stolpec] == 0


def naslednja_prosta_vrstica(mreza, stolpec):
    for v in range(st_vrstic):
        if mreza[v][stolpec] == 0:
            return v


def izpisi_mrezo(mreza):
    print(np.flip(mreza, 0))


def zmagovalna_poteza(mreza, barva):
    # preveri navpicno
    for s in range(st_stolpcev):
        for v in range(st_vrstic - 3):
            if mreza[v][s] == barva and mreza[v + 1][s] == barva and mreza[v + 2][s] == barva and mreza[v + 3][s] == barva:
                return True

    # preveri vodoravno
    for s in range(st_stolpcev - 3):
        for v in range(st_vrstic):
            if mreza[v][s] == barva and mreza[v][s + 1] == barva and mreza[v][s + 2] == barva and mreza[v][s + 3] == barva:
                return True

    # preveri diagonalo /
    for s in range(st_stolpcev - 3):
        for v in range(st_vrstic - 3):
            if mreza[v][s] == barva and mreza[v + 1][s + 1] == barva and mreza[v + 2][s + 2] == barva and mreza[v + 3][s + 3] == barva:
                return True

    # preveri diagonalo \
    for s in range(st_stolpcev - 3):
        for v in range(3, st_vrstic):
            if mreza[v][s] == barva and mreza[v - 1][s + 1] == barva and mreza[v - 2][s + 2] == barva and mreza[v - 3][s + 3] == barva:
                return True

def narisi_mrezo(mreza):
    for s in range(st_stolpcev):
        for v in range(st_vrstic):
            pygame.draw.rect(screen, BLUE, (s*kvadrat, v*kvadrat + kvadrat, kvadrat, kvadrat))
            pygame.draw.circle(screen, BLACK, (int(s*kvadrat + kvadrat/2), int(v*kvadrat + kvadrat + kvadrat/2)), rad)

    for s in range(st_stolpcev):
        for v in range(st_vrstic):
            if mreza[v][s] == 1:
                pygame.draw.circle(screen, PINK, (int(s*kvadrat + kvadrat/2), visina - int(v*kvadrat + kvadrat/2)), rad)
            elif mreza[v][s] == 2:
                pygame.draw.circle(screen, GREEN, (int(s*kvadrat + kvadrat/2), visina - int(v*kvadrat + kvadrat/2)), rad)
    pygame.display.update()


mreza = ustvari_mrezo()
izpisi_mrezo(mreza)
konec = False
turn = 0

pygame.init()

#velikost kvadratkov in krogcev
kvadrat = 100
rad = int(kvadrat/2 - 5)

sirina = st_stolpcev * kvadrat
visina = (st_vrstic + 1) * kvadrat

velikost = (sirina, visina)

screen = pygame.display.set_mode(velikost)
narisi_mrezo(mreza)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not konec:

    for poteza in pygame.event.get():
        if poteza.type == pygame.QUIT:
            sys.exit()

        if poteza.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, sirina, kvadrat))
            posx = poteza.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, PINK, (posx, int(kvadrat/2)), rad)
            else:
                pygame.draw.circle(screen, GREEN, (posx, int(kvadrat/2)), rad)
        pygame.display.update()

        if poteza.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, sirina, kvadrat))
            # na vrsti je 1.igralec
            if turn == 0:
                posx = poteza.pos[0]
                stolpec = int(math.floor(posx/kvadrat))

                if veljavna_poteza(mreza, stolpec):
                    vrstica = naslednja_prosta_vrstica(mreza, stolpec)
                    igraj(mreza, vrstica, stolpec, 1)

                    if zmagovalna_poteza(mreza, 1):
                        label = myfont.render("Zmaga!", 1, PINK)
                        screen.blit(label, (40, 10))
                        konec = True


            # na vrsti je 2.igralec
            else:
                posx = poteza.pos[0]
                stolpec = int(math.floor(posx/kvadrat))

                if veljavna_poteza(mreza, stolpec):
                    vrstica = naslednja_prosta_vrstica(mreza, stolpec)
                    igraj(mreza, vrstica, stolpec, 2)

                    if zmagovalna_poteza(mreza, 2):
                        label = myfont.render("Zmaga!", 1, GREEN)
                        screen.blit(label, (40, 10))
                        konec = True

            izpisi_mrezo(mreza)
            narisi_mrezo(mreza)

            turn += 1
            turn = turn % 2

            if konec:
                pygame.time.wait(3000)
