from planner.cutting.geometry import (Rectangle, dimensions_apres_rotation, est_dans, se_chevauchent)

# Fonction qui teste la fonction qui calcule la surface d'une pièce
def test_surface_rectangle():
    rectangle = Rectangle(
        x=0,
        y=0,
        largeur=400,
        longueur=800,
    )

    assert rectangle.surface == 320000

# Fonction qui teste si un rectangle entre dans un panneau
def test_rectangle_est_dans_le_panneau():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=2000,
        longueur=3000,
    )

    piece = Rectangle(
        x=100,
        y=200,
        largeur=400,
        longueur=800,
    )

    assert est_dans(piece, panneau)

# Fonction qui teste si un rectangle dépasse du panneau
def test_rectangle_depasse_du_panneau():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=2000,
        longueur=3000,
    )

    piece = Rectangle(
        x=1800,
        y=200,
        largeur=400,
        longueur=800,
    )

    assert not est_dans(piece, panneau)

# Fonction qui test si deux rectangles cote à cote se chevauchent
def test_rectangles_cote_a_cote_ne_se_chevauchent_pas():
    piece_a = Rectangle(
        x=0,
        y=0,
        largeur=400,
        longueur=800,
    )

    piece_b = Rectangle(
        x=400,
        y=0,
        largeur=300,
        longueur=800,
    )

    assert not se_chevauchent(piece_a, piece_b)

# Fonction qui teste si deux rectangles se chevauchent
def test_rectangles_qui_se_chevauchent():
    piece_a = Rectangle(
        x=0,
        y=0,
        largeur=400,
        longueur=800,
    )

    piece_b = Rectangle(
        x=200,
        y=300,
        largeur=300,
        longueur=500,
    )

    assert se_chevauchent(piece_a, piece_b)

# Fonction qui teste si une pièce n'est pas retournée
def test_rotation_non_retournee():
    assert dimensions_apres_rotation(
        largeur=400,
        longueur=800,
        retournee=False,
    ) == (400, 800)

# Fonction qui teste si une pièce est retournée
def test_rotation_retournee():
    assert dimensions_apres_rotation(
        largeur=400,
        longueur=800,
        retournee=True,
    ) == (800, 400)