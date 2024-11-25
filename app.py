import pyxel, random

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Nuit du c0de", fps=75)

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 60
vaisseau_y = 60

# vies
vies = 1

# initialisation des tirs
tirs_liste = []

# initialisation des ennemis
ennemis_liste = []

# initialisation des explosions
explosions_liste = []


def vaisseau_deplacement(x, y):
    """déplacement avec les touches de directions"""
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
    """création d'un tir avec la barre d'espace"""
    if pyxel.btnr(pyxel.KEY_SPACE):  # btnr pour éviter les tirs multiples
        tirs_liste.append([x + 4, y - 4])
    return tirs_liste


def tirs_deplacement(tirs_liste):
    """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""
    nouveaux_tirs = []
    for tir in tirs_liste:
        tir[1] -= 1
        if tir[1] >= -8:  # Garde les tirs dans la fenêtre
            nouveaux_tirs.append(tir)
    return nouveaux_tirs


def ennemis_creation(ennemis_liste):
    """création aléatoire des ennemis"""
    if pyxel.frame_count % 75 == 0:  # un ennemi par seconde
        ennemis_liste.append([random.randint(0, 120), 0])
    return ennemis_liste


def ennemis_deplacement(ennemis_liste):
    """déplacement des ennemis vers le bas et suppression s'ils sortent du cadre"""
    nouveaux_ennemis = []
    for ennemi in ennemis_liste:
        ennemi[1] += 1
        if ennemi[1] <= 128:  # Garde les ennemis dans la fenêtre
            nouveaux_ennemis.append(ennemi)
    return nouveaux_ennemis


def vaisseau_suppression(vies):
    """disparition du vaisseau et d'un ennemi si contact"""
    for ennemi in ennemis_liste:
        if ennemi[0] <= vaisseau_x + 8 and ennemi[1] <= vaisseau_y + 8 and ennemi[0] + 8 >= vaisseau_x and ennemi[1] + 8 >= vaisseau_y:
            ennemis_liste.remove(ennemi)
            vies = 0
    return vies


def ennemis_suppression():
    """disparition d'un ennemi et d'un tir si contact"""
    global explosions_liste
    for ennemi in ennemis_liste[:]:
        for tir in tirs_liste[:]:
            if ennemi[0] <= tir[0] + 1 and ennemi[0] + 8 >= tir[0] and ennemi[1] + 8 >= tir[1]:
                ennemis_liste.remove(ennemi)
                tirs_liste.remove(tir)
                # Ajout d'une explosion à la position de l'ennemi détruit
                explosions_liste.append([ennemi[0], ennemi[1], 0])  # Dernier élément : durée de l'explosion


def explosions_update():
    """mise à jour des explosions (augmentation de la durée et suppression quand fini)"""
    global explosions_liste
    nouvelles_explosions = []
    for explosion in explosions_liste:
        explosion[2] += 1  # Augmente la durée
        if explosion[2] < 15:  # Explosion visible pendant 15 frames
            nouvelles_explosions.append(explosion)
    explosions_liste = nouvelles_explosions


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables"""
    global vaisseau_x, vaisseau_y, tirs_liste, ennemis_liste, vies

    # mise à jour de la position du vaisseau
    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)

    # création des tirs en fonction de la position du vaisseau
    tirs_liste = tirs_creation(vaisseau_x, vaisseau_y, tirs_liste)

    # mise à jour des positions des tirs
    tirs_liste = tirs_deplacement(tirs_liste)

    # création des ennemis
    ennemis_liste = ennemis_creation(ennemis_liste)

    # mise à jour des positions des ennemis
    ennemis_liste = ennemis_deplacement(ennemis_liste)

    # suppression des ennemis et tirs si contact
    ennemis_suppression()

    # suppression du vaisseau et ennemi si contact
    vies = vaisseau_suppression(vies)

    # mise à jour des explosions
    explosions_update()


# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets"""
    if pyxel.btn(pyxel.KEY_Q):
        pyxel.quit()

    # vide la fenêtre
    pyxel.cls(0)

    # si le vaisseau possède des vies, le jeu continue
    if vies > 0:
        # vaisseau (carré 8x8)
        pyxel.rect(vaisseau_x, vaisseau_y, 8, 8, 1)

        # tirs
        for tir in tirs_liste:
            pyxel.rect(tir[0], tir[1], 1, 4, 10)

        # ennemis
        for ennemi in ennemis_liste:
            pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)

        # explosions
        for explosion in explosions_liste:
            pyxel.circ(explosion[0] + 4, explosion[1] + 4, explosion[2] // 2, 7)

    # sinon : GAME OVER
    else:
        pyxel.text(50, 64, 'GAME OVER', 7)


pyxel.run(update, draw)
