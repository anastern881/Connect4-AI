import numpy as np
import pygame
import sys
import math
import random

def ustvari_mrezo():
    mreza = np.zeros((st_vrstic, st_stolpcev))
    return mreza

def izpisi_mrezo(mreza):
    print(np.flip(mreza, 0))

def igraj(mreza, vrstica, stolpec, zeton):
    mreza[vrstica][stolpec] = zeton


def veljavna_poteza(mreza, stolpec):
    return mreza[st_vrstic - 1][stolpec] == 0


def naslednja_prosta_vrstica(mreza, stolpec):
    for v in range(st_vrstic):
        if mreza[v][stolpec] == 0:
            return v


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

def preglej_linijo(linija, zeton):
    tocke = 0
    nasprotni_zeton = zeton_igralec
    if zeton == zeton_igralec:
        nasprotni_zeton = zeton_racunalnik
    #preverimo vrednost linije
    if linija.count(zeton) == 4:
        tocke += 100
    elif linija.count(zeton) == 3 and linija.count(prazna) == 1:
        tocke += 5
    elif linija.count(zeton) == 2 and linija.count(prazna) == 2:
        tocke += 2

    if linija.count(nasprotni_zeton) == 3 and linija.count(prazna) == 1:
        tocke -= 4
    return tocke

def oceni_pozicijo(mreza, zeton):
    tocke = 0

    #sredinski stolpec
    srednji_stolpec = [int(i) for i in list(mreza[:, st_stolpcev//2])]
    tocke += srednji_stolpec.count(zeton) * 3

    #vodoravno
    for v in range(st_vrstic):
        vrstica = [int(i) for i in list(mreza[v,:])]
        for s in range(st_stolpcev-3):
            linija = vrstica[s:s+dolzina_linije]
            tocke += preglej_linijo(linija, zeton)
    #navpicno
    for s in range(st_stolpcev):
        stolpec = [int(i) for i in list(mreza[:,s])]
        for v in range(st_vrstic-3):
            linija = stolpec[v:v+dolzina_linije]
            tocke += preglej_linijo(linija, zeton)
    #diagonala /
    for v in range(st_vrstic-3):
        for s in range(st_stolpcev-3):
            linija = [mreza[v+i][s+i] for i in range(dolzina_linije)]
            tocke += preglej_linijo(linija, zeton)
    #diagonala \
    for v in range(st_vrstic-3):
        for s in range(st_stolpcev-3):
            linija = [mreza[v+3-i][s+i] for i in range(dolzina_linije)]
            tocke += preglej_linijo(linija, zeton)

    return tocke

def zaustavitveni_pogoj(mreza):
    return zmagovalna_poteza(mreza, zeton_igralec) or zmagovalna_poteza(mreza, zeton_racunalnik) or len(veljavne_lokacije(mreza)) == 0

def algoritem_minimax(mreza, globina, alfa, beta, isci_max):
    lokacije = veljavne_lokacije(mreza)
    ali_konec = zaustavitveni_pogoj(mreza)
    if globina == 0 or ali_konec:
        if ali_konec:
            if zmagovalna_poteza(mreza, zeton_racunalnik):
                return (None, 100000000000)
            elif zmagovalna_poteza(mreza, zeton_igralec):
                return (None, -100000000000)
            else:
                return (None, 0)
        elif globina == 0:
            return (None, oceni_pozicijo(mreza, zeton_racunalnik))
    if isci_max:
        tocke = -math.inf
        stolpec = random.choice(lokacije)
        for s in lokacije:
            vrstica = naslednja_prosta_vrstica(mreza, s)
            mreza2 = mreza.copy()
            igraj(mreza2, vrstica, s, zeton_racunalnik)
            nove_tocke = algoritem_minimax(mreza2, globina-1, alfa, beta, False)[1]
            if nove_tocke > tocke:
                tocke = nove_tocke
                stolpec = s
            alfa = max(alfa, tocke)
            if alfa >= beta:
                break
        return stolpec, tocke
    if not isci_max:
        tocke = math.inf
        stolpec = random.choice(lokacije)
        for s in lokacije:
            vrstica = naslednja_prosta_vrstica(mreza, s)
            mreza2 = mreza.copy()
            igraj(mreza2, vrstica, s, zeton_igralec)
            nove_tocke = algoritem_minimax(mreza2, globina-1, alfa, beta, True)[1]
            if nove_tocke < tocke:
                tocke = nove_tocke
                stolpec = s
            beta = min(beta, tocke)
            if alfa >= beta:
                break
        return stolpec, tocke

def veljavne_lokacije(mreza):
    lokacije = []
    for s in range(st_stolpcev):
        if veljavna_poteza(mreza, s):
            lokacije.append(s)
    return lokacije

def najboljsa_poteza(mreza, zeton):
    lokacije = veljavne_lokacije(mreza)
    naj_tocke = -10000
    naj_stolpec = random.choice(lokacije)
    for s in lokacije:
        vrstica = naslednja_prosta_vrstica(mreza, s)
        mreza2 = mreza.copy()
        igraj(mreza2, vrstica, s, zeton)
        tocke = oceni_pozicijo(mreza2, zeton)
        if tocke > naj_tocke:
            naj_tocke = tocke
            naj_stolpec = s
    return naj_stolpec

#velikost mreze
st_vrstic = 6
st_stolpcev = 7

igralec= 0
racunalnik=1

mreza = ustvari_mrezo()
izpisi_mrezo(mreza)
konec = False
na_vrsti = random.randint(igralec, racunalnik)

#vrednosti v mrezi
prazna=0
zeton_igralec=1
zeton_racunalnik=2

pygame.init()

#rgb barve
PINK = (230, 25, 97)
GREEN = (57, 255, 20)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

#velikost kvadratkov in krogcev
kvadrat = 100
rad = int(kvadrat/2 - 5)

sirina = st_stolpcev * kvadrat
visina = (st_vrstic + 1) * kvadrat

velikost = (sirina, visina)
dolzina_linije = 4

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
            if na_vrsti == igralec:
                pygame.draw.circle(screen, PINK, (posx, int(kvadrat/2)), rad)
            else:
                pygame.draw.circle(screen, GREEN, (posx, int(kvadrat/2)), rad)
        pygame.display.update()

        if poteza.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, sirina, kvadrat))
            # na vrsti je igralec
            if na_vrsti == igralec:
                posx = poteza.pos[0]
                stolpec = int(math.floor(posx/kvadrat))

                if veljavna_poteza(mreza, stolpec):
                    vrstica = naslednja_prosta_vrstica(mreza, stolpec)
                    igraj(mreza, vrstica, stolpec, zeton_igralec)

                    if zmagovalna_poteza(mreza, zeton_igralec):
                        label = myfont.render("Zmaga!", 1, PINK)
                        screen.blit(label, (40, 10))
                        konec = True
                    na_vrsti += 1
                    na_vrsti = na_vrsti % 2

                    izpisi_mrezo(mreza)
                    narisi_mrezo(mreza)

    # na vrsti je racunalnik
    if na_vrsti == racunalnik and not konec:
        stolpec, minimax_tocke = algoritem_minimax(mreza, 5, -math.inf, math.inf, True)

        if veljavna_poteza(mreza, stolpec):
            vrstica = naslednja_prosta_vrstica(mreza, stolpec)
            igraj(mreza, vrstica, stolpec, zeton_racunalnik)

            if zmagovalna_poteza(mreza, zeton_racunalnik):
                label = myfont.render("Zmaga!", 1, GREEN)
                screen.blit(label, (40, 10))
                konec = True

            izpisi_mrezo(mreza)
            narisi_mrezo(mreza)

            na_vrsti += 1
            na_vrsti = na_vrsti % 2

    if konec:
        pygame.time.wait(10000)
