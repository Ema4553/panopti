from planner.cutting.geometry import Rectangle
from planner.cutting.optimizer import optimiser_decoupe
from planner.services.metrics import (
    nombre_de_panneaux,
    surface_panneau,
    surface_pieces,
    surface_restante,
    taux_chute,
    taux_chute_global,
    taux_utilisation,
)
from planner.cutting.placement import Piece

def test_surface_pieces():
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
            largeur=400,
            longueur=400,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    panneau_utilise = resultat.panneaux[0]

    assert surface_pieces(panneau_utilise) == 520000

def test_surface_panneau():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Pièce",
            largeur=500,
            longueur=500,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert surface_panneau(resultat.panneaux[0]) == 1000000

def test_surface_restante():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Pièce",
            largeur=500,
            longueur=500,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert surface_restante(resultat.panneaux[0]) == 750000

def test_taux_utilisation():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Pièce",
            largeur=500,
            longueur=500,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert taux_utilisation(resultat.panneaux[0]) == 25.0

def test_taux_chute():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Pièce",
            largeur=500,
            longueur=500,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert taux_chute(resultat.panneaux[0]) == 75.0

def test_nombre_de_panneaux():
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

    assert nombre_de_panneaux(resultat.panneaux) == 2

def test_taux_chute_global():
    panneau = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    pieces = [
        Piece(
            designation="Pièce",
            largeur=500,
            longueur=500,
        ),
    ]

    resultat = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        rotation_autorisee=False,
    )

    assert taux_chute_global(resultat.panneaux) == 75.0
