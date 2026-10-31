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
        rotation_autorisee=False,
    )

    meilleur = choisir_meilleur_candidat(candidats)

    assert meilleur is not None
    assert meilleur.zone == zones[1]

# Fonction qui teste si la zone restante est bien réduite à cause du trait de coupe (épaisseur de lame)
def test_kerf_reduit_la_zone_restante():
    piece = Piece(
        designation="Pièce",
        largeur=600,
        longueur=400,
    )

    zone = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=[zone],
        rotation_autorisee=False,
    )

    assert len(candidats) == 1

# Fonction qui teste le cas où la pièce rentre pile avec le trait de coupe (épaisseur de lame)
def test_piece_rentre_avec_kerf_exact():
    piece = Piece(
        designation="Pièce",
        largeur=600,
        longueur=400,
    )

    zone = Rectangle(
        x=0,
        y=0,
        largeur=605,
        longueur=405,
    )

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=[zone],
        rotation_autorisee=False,
    )

    assert len(candidats) == 1

# Fonction qui teste le cas où la pièce a un grain dans la longueur, donc pas de rotation de la pièce autorisée
def test_grain_length_interdit_rotation_si_strict():
    piece = Piece(
        designation="Façade",
        largeur=400,
        longueur=800,
        grain_direction="length",
    )

    zone = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=[zone],
        rotation_autorisee=True,
        grain_strict=True,
    )

    assert len(candidats) == 1
    assert candidats[0].retournee is False

# Fonction qui teste le cas où la pièce a un grain dans la largeur, donc rotation de la pièce nécessaire
def test_grain_width_impose_rotation_si_strict():
    piece = Piece(
        designation="Façade",
        largeur=400,
        longueur=800,
        grain_direction="width",
    )

    zone = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=[zone],
        rotation_autorisee=True,
        grain_strict=True,
    )

    assert len(candidats) == 1
    assert candidats[0].retournee is True

# Fonction qui teste le cas où la pièce n'a pas de sens de grain défini (null/none), donc rotation autorisé
def test_grain_null_n_impose_aucune_orientation():
    piece = Piece(
        designation="Étagère",
        largeur=400,
        longueur=800,
        grain_direction=None,
    )

    zone = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=[zone],
        rotation_autorisee=True,
        grain_strict=True,
    )

    assert len(candidats) == 2

# Fonction
def test_grain_non_strict_autorise_rotation():
    piece = Piece(
        designation="Façade",
        largeur=400,
        longueur=800,
        grain_direction="length",
    )

    zone = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=[zone],
        rotation_autorisee=True,
        grain_strict=False,
    )

    assert len(candidats) == 2

# Fonction qui teste le cas où le grain est défini dans la largeur, et qu'il faut le respecter car grain_strict = true donc rend impossible le placement de la pièce
def test_grain_strict_et_rotation_interdite_rend_piece_impossible():
    piece = Piece(
        designation="Façade",
        largeur=400,
        longueur=800,
        grain_direction="width",
    )

    zone = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    candidats = trouver_candidats(
        piece=piece,
        zones_libres=[zone],
        rotation_autorisee=False,
        grain_strict=True,
    )

    assert candidats == []