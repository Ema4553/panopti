from planner.cutting.geometry import Rectangle
from planner.cutting.placement import Piece, peut_etre_placee

# Fonction qui teste si une pièce peut se placer dans un panneau vide
def test_piece_peut_etre_placee_dans_panneau_vide():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=2000,
        longueur=1000,
    )

    piece = Piece(
        designation="Étagère",
        largeur=400,
        longueur=800,
    )

    assert peut_etre_placee(
        piece=piece,
        panneau=panneau,
        placements_existants=[],
        x=0,
        y=0,
    )

# Fonction qui teste si une pièce peut être placée alors qu'elle sort du panneau
def test_piece_ne_peut_pas_sortir_du_panneau():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=2000,
        longueur=1000,
    )

    piece = Piece(
        designation="Étagère",
        largeur=400,
        longueur=800,
    )

    assert not peut_etre_placee(
        piece=piece,
        panneau=panneau,
        placements_existants=[],
        x=1800,
        y=0,
    )

# Fonction qui teste si une pièce en chevauche une autre déjà placée
def test_piece_ne_peut_pas_chevaucher_une_autre():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=2000,
        longueur=1000,
    )

    piece_a = Rectangle(
        x=0,
        y=0,
        largeur=800,
        longueur=400,
    )

    piece_b = Piece(
        designation="Étagère B",
        largeur=400,
        longueur=300,
    )

    assert not peut_etre_placee(
        piece=piece_b,
        panneau=panneau,
        placements_existants=[piece_a],
        x=200,
        y=100,
    )

# Fonction qui teste si une pièce peut être placée à côté
def test_piece_peut_etre_placee_a_cote():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=2000,
        longueur=1000,
    )

    piece_a = Rectangle(
        x=0,
        y=0,
        largeur=800,
        longueur=400,
    )

    piece_b = Piece(
        designation="Étagère B",
        largeur=400,
        longueur=300,
    )

    assert peut_etre_placee(
        piece=piece_b,
        panneau=panneau,
        placements_existants=[piece_a],
        x=800,
        y=0,
    )

# Fonction qui teste si une pièce retournée peut être placée
def test_piece_peut_etre_retournee():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=500,
        longueur=1000,
    )

    piece = Piece(
        designation="Pièce longue",
        largeur=800,
        longueur=400,
    )

    assert not peut_etre_placee(
        piece=piece,
        panneau=panneau,
        placements_existants=[],
        x=0,
        y=0,
        retournee=False,
    )

    assert peut_etre_placee(
        piece=piece,
        panneau=panneau,
        placements_existants=[],
        x=0,
        y=0,
        retournee=True,
    )