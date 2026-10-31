from planner.cutting.geometry import Rectangle
from planner.cutting.optimizer import optimiser_decoupe, trier_pieces
from planner.cutting.placement import Piece


def test_trier_pieces_par_surface_decroissante():
    pieces = [
        Piece(designation="Petite", largeur=300, longueur=300),
        Piece(designation="Grande", largeur=800, longueur=600),
        Piece(designation="Moyenne", largeur=500, longueur=400),
    ]

    pieces_triees = trier_pieces(pieces)

    assert [piece.designation for piece in pieces_triees] == [
        "Grande",
        "Moyenne",
        "Petite",
    ]


def test_optimizer_place_toutes_les_pieces_sur_un_panneau():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Grand panneau",
            largeur=600,
            longueur=600,
        ),
        Piece(
            designation="Petite pièce",
            largeur=400,
            longueur=400,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert len(resultat.panneaux) == 1
    assert len(resultat.panneaux[0].placements) == 2
    assert resultat.pieces_non_placees == []


def test_optimizer_ouvre_un_deuxieme_panneau():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Pièce 1",
            largeur=600,
            longueur=600,
        ),
        Piece(
            designation="Pièce 2",
            largeur=600,
            longueur=600,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert len(resultat.panneaux) == 2
    assert len(resultat.pieces_non_placees) == 0

    assert len(resultat.panneaux[0].placements) == 1
    assert len(resultat.panneaux[1].placements) == 1


def test_optimizer_signale_piece_trop_grande():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    piece = Piece(
        designation="Trop grande",
        largeur=1200,
        longueur=500,
    )

    resultat = optimiser_decoupe(
        pieces=[piece],
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert len(resultat.panneaux) == 0
    assert resultat.pieces_non_placees == [piece]


def test_optimizer_utilise_la_rotation():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=600,
        longueur=1000,
    )

    piece = Piece(
        designation="Pièce à retourner",
        largeur=800,
        longueur=400,
    )

    resultat = optimiser_decoupe(
        pieces=[piece],
        panneau=panneau,
        rotation_autorisee=True,
    )

    assert len(resultat.panneaux) == 1
    assert len(resultat.panneaux[0].placements) == 1

    placement = resultat.panneaux[0].placements[0]

    assert placement.retournee is True
    assert placement.largeur == 400
    assert placement.longueur == 800

# Fonction qui teste si le nombre de panneau augmente en prenant en compte le trait de coupe (épaisseur de lame)
def test_optimizer_prend_en_compte_le_kerf():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Pièce 1",
            largeur=600,
            longueur=1000,
        ),
        Piece(
            designation="Pièce 2",
            largeur=396,
            longueur=1000,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
        epaisseur_lame=5,
    )

    assert len(resultat.panneaux) == 2


def test_optimizer_respecte_grain_avec_rotation_autorisee():
    piece = Piece(
        designation="Façade",
        largeur=600,
        longueur=400,
        grain_direction="width",
    )

    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=700,
    )

    resultat = optimiser_decoupe(
        pieces=[piece],
        panneau=panneau,
        rotation_autorisee=True,
        grain_strict=True,
    )

    assert len(resultat.panneaux) == 1
    assert len(resultat.pieces_non_placees) == 0

    placement = resultat.panneaux[0].placements[0]

    assert placement.retournee is True
    assert placement.largeur == 400
    assert placement.longueur == 600


def test_optimizer_ne_place_pas_piece_si_grain_incompatible():
    piece = Piece(
        designation="Façade",
        largeur=600,
        longueur=400,
        grain_direction="width",
    )

    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=700,
    )

    resultat = optimiser_decoupe(
        pieces=[piece],
        panneau=panneau,
        rotation_autorisee=False,
        grain_strict=True,
    )

    assert len(resultat.panneaux) == 0
    assert len(resultat.pieces_non_placees) == 1
    assert resultat.pieces_non_placees[0] == piece

def test_optimizer_prend_en_compte_epaisseur_lame():
    pieces = [
        Piece(designation="Côté gauche", largeur=600, longueur=400),
        Piece(designation="Côté droit", largeur=600, longueur=400),
    ]

    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=800,
    )

    resultat_sans_kerf = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
        epaisseur_lame=0,
    )

    resultat_avec_kerf = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
        epaisseur_lame=5,
    )

    assert len(resultat_sans_kerf.panneaux) == 1
    assert len(resultat_avec_kerf.panneaux) == 2