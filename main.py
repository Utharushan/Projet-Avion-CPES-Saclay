from time import *
import pygame
import traceback
from pygame.locals import *
from test import *
from random import randint, choice
import string


def pause_jeu(fenetre):
    """
    Prend en entrée un argument fenetre de pygame
    ------------------------------------------------------------------------------------------------
    Met le jeu en pause jusqu'à ce que l'utilisateur appuie sur ESPACE
    ------------------------------------------------------------------------------------------------
    """
    pause = 1
    while pause:
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONDOWN:
                (x,y)=event.pos
            if event.type==KEYDOWN:
                if event.key == K_SPACE:
                    pause = 0


def genere_id():
    """
    ------------------------------------------------------------------------------------------------
    Génère un identifiant alphanumérique pour un avion
    ------------------------------------------------------------------------------------------------
    Renvoie une chaîne de caractères de 6 caractères aléatoires
    """
    chaine = string.ascii_letters + string.digits
    indicatif = ''.join(choice(chaine) for i in range(6))
    return indicatif


def generer_avion(tas):
    """
    Prend en entrée un objet de type TAS
    ------------------------------------------------------------------------------------------------
    Crée un avion avec des attributs aléatoires et l'ajoute dans le tas
    ------------------------------------------------------------------------------------------------
    Renvoie le tas mis à jour avec l’avion ajouté
    """
    pirate, feu, heures = randint(1, 15), randint(1, 15), randint(1, 18)
    ID = genere_id()
    if pirate in (1, 2, 3): # 3 chances sur 15 d'être piraté
        pirate = True
    else:
        pirate = False
    if feu in (1, 2):  # 2 chances sur 15
        feu = True
    else:
        feu = False
    avion = Avion(ID, heures, pirate, feu)
    tas = tas.ajouter(avion)
    return tas

def simulate_landing_animation(fenetre, avion_image, tab, tab_atterris, t_detourne, tas, debut):
    """
    Prend en entrée un argument fenetre de pygame, une image avion,
    et des listes pour les avions en file d’attente, atterris, et détournés,
    un objet de type TAS, un int debut pour le bandeau
    ------------------------------------------------------------------------------------------------
    Simule une animation d’atterrissage de l’avion et met à jour les listes
    d’avions
    ------------------------------------------------------------------------------------------------
    Renvoie le tas et l'int debut mis à jour
    """
    clock = pygame.time.Clock()
    x_pos = -125
    y_pos = 180   
    width, height = 150, 75  
    landing_speed = 2.5  
    angle_rota = 20  
    max_rota = 8
    cpt = 0

    background = pygame.image.load("images/fotor grand tab couvert.png").convert_alpha()
    background_resized = pygame.transform.scale(background, (1080, 720))
    fond2 = pygame.image.load("images/fond interieur.png").convert_alpha()
    fond_resized2 = pygame.transform.scale(fond2, (1080, 720))
    while x_pos < 1080:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                (x, y) = event.pos
                if 16 <= x <= 166 and 235 <= y <= 300:
                    tas = generer_avion(tas)
                    tas, tab = maj(tas, tab)
                if 940 <= x <= 1070 and 230 <= y <= 290:
                    x_pos = 2000
            if event.type == QUIT:
                x_pos = 2000
                tas = Vide()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    x_pos = 2000
                    tas = Vide()
                elif event.key == K_LEFT:
                    tas = generer_avion(tas)
                    tas, tab = maj(tas, tab)
                elif event.key == K_RIGHT:
                    x_pos = 2000
                elif event.key == K_SPACE:
                    pause_jeu(fenetre)
                    
    
        if y_pos >= 345:  
            if angle_rota > max_rota:  
                angle_rota -= 1  

        avion_resized = pygame.transform.scale(avion_image, (width, height))
        avion_rotate = pygame.transform.rotate(avion_resized, angle_rota)
        
        fenetre.blit(background_resized, (0, 0))
        fenetre.blit(avion_rotate, (x_pos, y_pos))
        fenetre.blit(fond_resized2, (0, 0))

        afficher_liste_avions(fenetre, tab)
        afficher_avions_atterris(fenetre, tab_atterris)
        afficher_avions_detournes(fenetre, t_detourne)
        debut = bandeau(fenetre, debut, cpt)
        cpt += 1
        
            
        if y_pos <= 380:
            y_pos += landing_speed * 2 
            width += 2 * landing_speed  
            height += landing_speed  
            x_pos += landing_speed * 1.5
        x_pos += landing_speed * 3

        pygame.display.flip()
        clock.tick(20)
    return tas, debut


def simulate_landing(tas, debut, fenetre, tab, tab_atterris, t_detourne):
    """
    Prend en entrée un objet de type TAS, un int debut, un argument fenetre de
    pygame, et des listes pour les avions en file d’attente, atterris, et
    détournés
    ------------------------------------------------------------------------------------------------
    Simule l’atterrissage du premier avion du tas avec animation
    ------------------------------------------------------------------------------------------------
    Renvoie le tas et l'int debut mis à jour
    """
    plane = tas.minimum()
    if plane.F:
        avion_image = pygame.image.load("images/avions/avion_feu.png").convert_alpha()
    elif plane.P:
        avion_image = pygame.image.load("images/avions/avion_pirate.png").convert_alpha()
    elif plane.H <= 3:
        avion_image = pygame.image.load("images/avions/avion_carburant.png").convert_alpha()
    else:
        avion_image = pygame.image.load("images/avions/avion.png").convert_alpha()
    tas, debut = simulate_landing_animation(fenetre, avion_image, tab, tab_atterris, t_detourne, tas, debut)
    return tas, debut

def afficher_liste_avions(fenetre, tab):
    """
    Prend en entrée un argument fenetre de pygame et une liste tab contenant les
    avions en attente
    ------------------------------------------------------------------------------------------------
    Affiche la liste des avions en attente d'atterrissage avec leurs indicateurs
    de priorité (feu, carburant faible, pirate) et le nombre d’avions restants
    si plus de 5
    ------------------------------------------------------------------------------------------------
    """
    titre = "Atterrissages"
    font = pygame.font.SysFont("arial black", 20, bold = False, italic=False) 
    text = font.render(titre, 1, (0, 0, 0))
    fenetre.blit(text, (240, 50))
    
    pirate = pygame.image.load("images/urgence/pirate.png").convert_alpha()
    feu = pygame.image.load("images/urgence/feu.png").convert_alpha()
    carburant = pygame.image.load("images/urgence/carburant.png").convert_alpha()
    probleme = pygame.image.load("images/urgence/probleme.png").convert_alpha()
    dico_etat = {"pirate" : pirate, "feu" : feu, "carburant" : carburant}

    x = 212
    y = 90
    for i in range(len(tab[:5])):
        count = 0
        chaine = f"Avion {tab[i].ind}"
        font = pygame.font.SysFont("Arial black", 16, bold = False, italic=False) 
        text = font.render(chaine, 1, (0, 0, 0))

        chaine = f"{i+1}."
        font = pygame.font.SysFont("arial black", 16, bold = False, italic=False) 
        texte = font.render(chaine, 1, (0, 0, 0))
        fenetre.blit(texte, (192, y + 30*i))
        
        if tab[i].F:
            image_reduite = pygame.transform.scale(feu, (25, 25))
            fenetre.blit(image_reduite,(x + 35*count, y + 30*i))
            count += 1
        if tab[i].H <= 3:
            image_reduite = pygame.transform.scale(carburant, (25, 25))
            fenetre.blit(image_reduite,(x + 35*count, y + 30*i))
            count += 1
        if tab[i].P:
            image_reduite = pygame.transform.scale(pirate, (25, 25))
            fenetre.blit(image_reduite,(x + 35*count, y + 30*i))
            count += 1
        fenetre.blit(text, (x + 33*count, y + 30*i))
    if len(tab) > 5:
        reste = len(tab) -5
        chaine = f"{reste} autres avions restants"
        font = pygame.font.SysFont("arial black", 12, bold = False, italic=False) 
        texte = font.render(chaine, 1, (0, 0, 0))
        fenetre.blit(texte, (235, 240))

        
def afficher_avions_atterris(fenetre, tab_atterris):
    """
    Prend en entrée un argument fenetre de pygame et une liste tab_atterris
    contenant les avions ayant atterris
    ------------------------------------------------------------------------------------------------
    Affiche la liste des avions récemment atterris (jusqu'à 5 derniers) avec un
    marquage pour l’avion le plus récent, ainsi que le nombre total
    d'atterrissages
    ------------------------------------------------------------------------------------------------
    """
    titre = "Atterris"
    font = pygame.font.SysFont("arial black", 20, bold = False, italic=False) 
    text = font.render(titre, 1, (0, 0, 0))
    fenetre.blit(text, (510, 50))
    n = len(tab_atterris)
    tab_atterris = tab_atterris[-5:][::-1]
    for i in range(len(tab_atterris)):
        if i == 0:
            bonus = " - à l'instant"
        else:
            bonus = ""
        chaine = f"Avion {tab_atterris[i].ind}" + bonus
        font = pygame.font.SysFont("arial black", 14, bold = False, italic=False) 
        text = font.render(chaine, 1, (0, 0, 0))
        fenetre.blit(text, (460, 90 + 30*i))
        chaine = f"{n} atterrissages"
        font = pygame.font.SysFont("arial black", 12, bold = False, italic=False) 
        texte = font.render(chaine, 1, (0, 0, 0))
        fenetre.blit(texte, (510, 240))


def afficher_avions_detournes(fenetre, t_detourne):
    """
    Prend en entrée un argument fenetre de pygame et une liste t_detourne
    contenant les avions détournés
    ------------------------------------------------------------------------------------------------
    Affiche la liste des avions récemment détournés (jusqu'à 5 derniers) avec
    un marquage pour l’avion le plus récent, ainsi que le nombre total d'avions
    détournés
    ------------------------------------------------------------------------------------------------
    """
    titre = "Détournés"
    font = pygame.font.SysFont("arial black", 20, bold = False, italic=False) 
    text = font.render(titre, 1, (0, 0, 0))
    fenetre.blit(text, (725, 50))
    
    n = len(t_detourne)
    t_detourne = t_detourne[-5:][::-1]
    for i in range(len(t_detourne)):
        if i == 0:
            bonus = " - à l'instant"
        else:
            bonus = ""
        chaine = f"Avion {t_detourne[i].ind}" + bonus 
        font = pygame.font.SysFont("arial black", 14, bold = False, italic=False) 
        text = font.render(chaine, 1, (0, 0, 0))
        fenetre.blit(text, (685, 90 + 30*i))
        chaine = f"{n} avions détournés"
        font = pygame.font.SysFont("arial black", 12, bold = False, italic=False) 
        texte = font.render(chaine, 1, (0, 0, 0))
        fenetre.blit(texte, (725, 240))


def afficher_fin(fenetre):
    """
    Prend en entrée un argument fenetre de pygame
    ------------------------------------------------------------------------------------------------
    Affiche un message "AEROPORT FERME" indiquant la fermeture de l’aéroport
    ------------------------------------------------------------------------------------------------
    """
    chaine = "AEROPORT"
    chaine2 = "FERME !"
    font = pygame.font.SysFont("arial", 54, bold = True, italic=False) 
    text = font.render(chaine, 1, (0, 0, 0))
    text2 = font.render(chaine2, 1, (0, 0, 0))
    fenetre.blit(text, (420, 110))
    fenetre.blit(text2, (455, 170))
    


def bandeau(fenetre, debut, cpt, delai=2):
    """
    Prend en entrée un argument fenetre de pygame, un entier debut pour le début
    de texte, un compteur cpt, et un int delai
    ------------------------------------------------------------------------------------------------
    Affiche un message défilant sur la fenêtre Pygame concernant les
    instructions d’embarquement et fait défiler le texte en fonction de delai
    ------------------------------------------------------------------------------------------------
    Renvoie un entier debut mis à jour pour le défilement du texte
    """
    p0 = "                    "  # 20 espaces
    p1 = "Veuillez vous présenter à la porte d'embarquement au moins 30 minutes avant l'horaire de départ. "
    p2 = "Si vous n'arrivez pas 10 minutes avant l'heure de départ, vous ne pourrez pas embarquer."
    chaine = p0 + p1 + p2
    n = len(chaine)
    assert n == 205, "La longueur totale n'est pas de 205 caractères"
    if debut + 78 <= n:
        texte_affiche = chaine[debut : debut + 78]
    else:
        texte_affiche = chaine[debut:] + chaine[:(debut + 78) % n]
    font = pygame.font.SysFont("couriernew", 14, bold=True, italic=False)
    text = font.render(texte_affiche, 1, (255, 255, 255))
    fenetre.blit(text, (235, 270))
    if cpt % delai == 0:
        debut = (debut + 1) % n
    return debut


def liste_avion_pirate(liste_tas):
    """
    Prend en entrée une liste liste_tas d’avions
    ------------------------------------------------------------------------------------------------
    Parcourt la liste d'avions et renvoie une liste contenant les avions
    marqués comme piratés
    ------------------------------------------------------------------------------------------------
    Renvoie une liste des avions piratés de liste_tas
    """
    t = []
    for i in range(len(liste_tas)):
        if liste_tas[i].P:
            t.append(liste_tas[i])
    return t


def maj(tas, tab):
    """
    Prend en entrée un objet tas et une liste tab d’avions
    ------------------------------------------------------------------------------------------------
    Met à jour la liste des avions à partir du tas, vérifie l'ordre des
    priorités, et garantit que le minimum est à la bonne place
    ------------------------------------------------------------------------------------------------
    Renvoie le tas et la liste mise à jour des avions tab
    """
    tab = tas.tas_to_liste()            
    if len(tab) > 0: assert tab[0] == tas.minimum(), "PAS BIEN TRIE"
    return tas, tab


def interface(tas):
    """
    Prend en entrée un objet de type tas représentant la liste d’attente des
    avions
    ------------------------------------------------------------------------------------------------
    Gère l'interface graphique principale pour l’aéroport, en permettant la
    visualisation et gestion des avions en attente, atterris, ou détournés
    ------------------------------------------------------------------------------------------------
    """
    pygame.init()
    try:
        fenetre = pygame.display.set_mode((1080, 720))
        fenetre.fill((255, 255, 255))
        fond = pygame.image.load("images/fotor grand tab couvert.png")
        fond2 = pygame.image.load("images/fond interieur.png").convert_alpha()

        fond_resized = pygame.transform.scale(fond,(1080, 720))
        fond_resized2 = pygame.transform.scale(fond2,(1080, 720))

        tab_atterris = []
        t_detourne = []
        debut = 0
        continuer = True
        while continuer:
            tab = tas.tas_to_liste()            
            tas, tab = maj(tas, tab)
            liste_pirate = liste_avion_pirate(tab)
            for avion in liste_pirate:
                tas, tab, t_detourne = tas.detourne(avion, t_detourne)

            fenetre.blit(fond_resized, (0, 0))
            fenetre.blit(fond_resized2, (0, 0))
            
            if tas.taille() > 0:
                avion_atterri = tab[0]
                tas, debut = simulate_landing(tas, debut, fenetre, tab, tab_atterris, t_detourne)
                tab_atterris.append(avion_atterri)
                tas = tas.supprimer_avion(avion_atterri.ind)

            else:
                fond2 = pygame.image.load("images/fond interieur 2.png").convert_alpha()
                fond_resized2 = pygame.transform.scale(fond2,(1080, 720))           

            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    (x,y)=event.pos
                    if 16 <= x <= 166 and 235 <= y <= 300:
                        tas = generer_avion(tas)
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        tas = generer_avion(tas)
                        tas, tab = maj(tas, tab)
                        
                if event.type == QUIT :
                    continuer = 0
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        continuer = 0
            
            if tas.taille() == 0:
                afficher_fin(fenetre)
            pygame.display.flip()
    except:
        traceback.print_exc()
    finally:
        pygame.quit()
        exit()

tas = Vide()
for i in range(10):
    tas = generer_avion(tas)

interface(tas)
