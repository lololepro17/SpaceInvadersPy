import pyxel
import random

# Taille de la fenêtre
pyxel.init(128, 128, title="Nuit du c0de", fps=75)
pyxel.load("PYXEL_RESOURCE_FILE.pyxres")

# Variables globales
vaisseau_x = 60
vaisseau_y = 100
vies = 10
tirs_liste = []
ennemis_liste = []
missiles_ennemis_liste = []
explosions_liste = []


def reset_game():
    """Réinitialisation des variables du jeu"""
    global vaisseau_x, vaisseau_y, vies, tirs_liste, ennemis_liste, missiles_ennemis_liste, explosions_liste
    vaisseau_x = 60
    vaisseau_y = 100
    vies = 10
    tirs_liste = []
    ennemis_liste = []
    missiles_ennemis_liste = []
    explosions_liste = []


def vaisseau_deplacement(x, y):
    """Déplacement avec les touches de direction"""
    if pyxel.btn(pyxel.KEY_RIGHT) and x < 120:
        x += 1
    if pyxel.btn(pyxel.KEY_LEFT) and x > 0:
        x -= 1
    if pyxel.btn(pyxel.KEY_DOWN) and y < 120:
        y += 1
    if pyxel.btn(pyxel.KEY_UP) and y > 0:
        y -= 1
    return x, y


def tirs_creation(x, y, tirs_liste):
    """Création d'un tir avec la barre d'espace"""
    if pyxel.btnr(pyxel.KEY_SPACE):  # btnr pour éviter les tirs multiples
        tirs_liste.append([x + 4, y - 4])
    return tirs_liste


def tirs_deplacement(tirs_liste):
    """Déplacement des tirs vers le haut"""
    nouveaux_tirs = []
    for tir in tirs_liste:
        tir[1] -= 2
        if tir[1] >= -8:
            nouveaux_tirs.append(tir)
    return nouveaux_tirs


def ennemis_creation(ennemis_liste):
    """Création aléatoire des ennemis"""
    if pyxel.frame_count % 120 == 0:  # Un ennemi toutes les 120 frames
        ennemis_liste.append(
            [random.randint(0, 112), 0, random.randint(0, 6)]
        )  # Ajout type ennemi
    return ennemis_liste


def ennemis_deplacement(ennemis_liste):
    """Déplacement des ennemis vers le bas"""
    nouveaux_ennemis = []
    for ennemi in ennemis_liste:
        ennemi[1] += 0.25  # Les ennemis avancent encore plus lentement
        if ennemi[1] <= 128:
            nouveaux_ennemis.append(ennemi)
    return nouveaux_ennemis


def ennemis_atteignent_bas(ennemis_liste, vies):
    """Réduit les vies si un ennemi atteint le bas de l'écran"""
    for ennemi in ennemis_liste[:]:
        if ennemi[1] >= 128:  # Si un ennemi sort de l'écran
            ennemis_liste.remove(ennemi)
            vies -= 1
    return vies


def ennemis_tir(missiles_ennemis_liste):
    """Ajout de tirs d'ennemis correspondant à leur type avec des probabilités aléatoires"""
    for ennemi in ennemis_liste:
        if random.randint(1, 300) < 5:  # chance de tirer par ennemi à chaque frame
            type_ennemi = ennemi[2]
            missiles_ennemis_liste.append([ennemi[0] + 4, ennemi[1] + 8, type_ennemi])
    return missiles_ennemis_liste


def missiles_deplacement(missiles_ennemis_liste):
    """Déplacement des missiles ennemis"""
    nouveaux_missiles = []
    for missile in missiles_ennemis_liste:
        missile[1] += 1  # Les missiles avancent plus lentement
        if missile[1] <= 128:
            nouveaux_missiles.append(missile)
    return nouveaux_missiles


def ennemis_suppression():
    """Suppression des ennemis et tirs en cas de collision"""
    global explosions_liste
    for ennemi in ennemis_liste[:]:
        for tir in tirs_liste[:]:
            if (
                ennemi[0] <= tir[0] + 4
                and ennemi[0] + 16 >= tir[0]
                and ennemi[1] + 16 >= tir[1]
            ):
                ennemis_liste.remove(ennemi)
                tirs_liste.remove(tir)
                explosions_liste.append([ennemi[0], ennemi[1], 0])  # Nouvelle explosion


def vaisseau_suppression(vies):
    """Suppression du vaisseau en cas de collision avec un ennemi ou un missile"""
    for ennemi in ennemis_liste:
        if (
            ennemi[0] <= vaisseau_x + 8
            and ennemi[1] <= vaisseau_y + 8
            and ennemi[0] + 16 >= vaisseau_x
            and ennemi[1] + 16 >= vaisseau_y
        ):
            ennemis_liste.remove(ennemi)
            vies -= 1
    for missile in missiles_ennemis_liste:
        if (
            missile[0] <= vaisseau_x + 8
            and missile[1] <= vaisseau_y + 8
            and missile[0] + 4 >= vaisseau_x
            and missile[1] + 8 >= vaisseau_y
        ):
            missiles_ennemis_liste.remove(missile)
            vies -= 1
    return vies


def explosions_update():
    """Mise à jour des explosions avec une animation plus lente"""
    global explosions_liste
    nouvelles_explosions = []
    for explosion in explosions_liste:
        if pyxel.frame_count % 5 == 0:  # Réduction de la vitesse d'animation
            explosion[2] += 1
        if explosion[2] < 4:  # Animation sur 4 frames
            nouvelles_explosions.append(explosion)
    explosions_liste = nouvelles_explosions


def update():
    """Mise à jour des variables"""
    global vaisseau_x, vaisseau_y, tirs_liste, ennemis_liste, missiles_ennemis_liste, vies

    if pyxel.btn(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnr(pyxel.KEY_R) and vies == 0:
        reset_game()

    if vies > 0:
        vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)
        tirs_liste = tirs_creation(vaisseau_x, vaisseau_y, tirs_liste)
        tirs_liste = tirs_deplacement(tirs_liste)
        ennemis_liste = ennemis_creation(ennemis_liste)
        ennemis_liste = ennemis_deplacement(ennemis_liste)
        vies = ennemis_atteignent_bas(ennemis_liste, vies)
        missiles_ennemis_liste = ennemis_tir(missiles_ennemis_liste)
        missiles_ennemis_liste = missiles_deplacement(missiles_ennemis_liste)
        ennemis_suppression()
        vies = vaisseau_suppression(vies)
        explosions_update()


def draw():
    """Affichage des objets"""
    pyxel.cls(0)
    if vies > 0:
        pyxel.blt(vaisseau_x, vaisseau_y, 0, 48, 0, 16, 16, 0)
        for tir in tirs_liste:
            pyxel.blt(tir[0], tir[1], 0, 48, 16, 8, 8, 0)
        for ennemi in ennemis_liste:
            type_ennemi = ennemi[2]
            pyxel.blt(ennemi[0], ennemi[1], 1, type_ennemi * 16, 0, 16, 16, 0)
        for missile in missiles_ennemis_liste:
            type_missile = missile[2]
            pyxel.blt(missile[0], missile[1], 0, type_missile * 16, 16, 8, 8, 0)
        for explosion in explosions_liste:
            frame = explosion[2] * 16
            pyxel.blt(explosion[0], explosion[1], 0, frame, 24, 16, 16, 0)
        pyxel.text(5, 5, f"VIES: {vies}", 7)
    else:
        pyxel.text(40, 60, "GAME OVER", 7)
        pyxel.text(30, 80, "Appuyez sur R pour relancer", 7)


pyxel.run(update, draw)
