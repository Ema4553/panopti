from planner.cutting.geometry import Rectangle
from planner.cutting.placement import Piece, peut_etre_placee, trouver_candidats, choisir_meilleur_candidat

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


# Fonction qui teste si des pièces peuvent rentrer dans une zone en les tournant
def test_trouver_candidats_avec_rotation():
    piece = Piece(
        designation="Pièce longue",
        largeur=800,
        longueur=400,
    )

    zones = [
        Rectangle(
            x=0,
            y=0,
            largeur=500,
            longueur=1000,
        )
    ]

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=zones,
        placements_existants=[],
        rotation_autorisee=True,
    )

    assert len(candidats) == 1
    assert candidats[0].retournee is True
    assert candidats[0].largeur == 400
    assert candidats[0].longueur == 800


# Fonction qui teste si des pièces peuvent rentrer dans une zone sans les tourner
def test_trouver_candidats_sans_rotation():
    piece = Piece(
        designation="Pièce longue",
        largeur=800,
        longueur=400,
    )

    zones = [
        Rectangle(
            x=0,
            y=0,
            largeur=500,
            longueur=1000,
        )
    ]

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=zones,
        placements_existants=[],
        rotation_autorisee=False,
    )

    assert candidats == []


# Fonction qui teste laquelle des possiblité de placement est la meilleure : BEST FIT
def test_choisir_meilleur_candidat():
    piece = Piece(
        designation="Étagère",
        largeur=400,
        longueur=800,
    )

    zones = [
        Rectangle(
            x=0,
            y=0,
            largeur=1000,
            longueur=1000,
        ),
        Rectangle(
            x=1000,
            y=0,
            largeur=500,
            longueur=900,
        ),
    ]

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=zones,
        placements_existants=[],
        rotation_autorisee=False,
    )

    meilleur = choisir_meilleur_candidat(candidats)

    assert meilleur is not None
    assert meilleur.zone == zones[1]