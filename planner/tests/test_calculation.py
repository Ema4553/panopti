import pytest
from planner.models import Projet, PanneauType, PieceRequise, OptionsDeCoupe
from planner.services.calculation import construire_pieces, construire_panneau, construire_parametres_coupe

@pytest.fixture
def projet_avec_panneau(db):
    panneau = PanneauType.objects.create(
        nom="Mélaminé blanc",
        longueur=2500,
        largeur=1250,
        epaisseur=18,
    )

    return Projet.objects.create(
        nom="Meuble de cuisine",
        description="Projet de test",
        panneau_type=panneau,
    )

@pytest.mark.django_db
def test_construire_pieces_avec_quantite_unitaire(projet_avec_panneau):
    PieceRequise.objects.create(
        projet=projet_avec_panneau,
        designation="Côté",
        longueur=600,
        largeur=400,
        epaisseur=18,
        quantite=1,
    )

    pieces = construire_pieces(projet_avec_panneau)

    assert len(pieces) == 1
    assert pieces[0].designation == "Côté"
    assert pieces[0].largeur == 400
    assert pieces[0].longueur == 600
    assert pieces[0].numero_exemplaire_piece == 1

@pytest.mark.django_db
def test_construire_pieces_decompose_quantite(projet_avec_panneau):
    PieceRequise.objects.create(
        projet=projet_avec_panneau,
        designation="Côté",
        longueur=600,
        largeur=400,
        epaisseur=18,
        quantite=3,
    )

    pieces = construire_pieces(projet_avec_panneau)

    assert len(pieces) == 3
    assert [piece.numero_exemplaire_piece for piece in pieces] == [1, 2, 3]


@pytest.mark.django_db
def test_construire_pieces_gere_plusieurs_references(projet_avec_panneau):
    PieceRequise.objects.create(
        projet=projet_avec_panneau,
        designation="Côté",
        longueur=600,
        largeur=400,
        epaisseur=18,
        quantite=2,
    )

    PieceRequise.objects.create(
        projet=projet_avec_panneau,
        designation="Fond",
        longueur=800,
        largeur=500,
        epaisseur=18,
        quantite=3,
    )

    pieces = construire_pieces(projet_avec_panneau)

    assert len(pieces) == 5
    assert sum(piece.designation == "Côté" for piece in pieces) == 2
    assert sum(piece.designation == "Fond" for piece in pieces) == 3


@pytest.mark.django_db
def test_construire_panneau_depuis_projet(projet_avec_panneau):
    panneau = construire_panneau(projet_avec_panneau)

    assert panneau.x == 0
    assert panneau.y == 0
    assert panneau.largeur == 1250
    assert panneau.longueur == 2500


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("epaisseur_lame", "attendu"),
    [
        ("3", 3),
        ("5", 5),
    ],
)
def test_construire_parametres_convertit_epaisseur_lame(
    projet_avec_panneau,
    epaisseur_lame,
    attendu,
):
    options = OptionsDeCoupe.objects.create(
        projet=projet_avec_panneau,
        epaisseur_lame=epaisseur_lame,
        rotation_autorisee=True,
        grain_strict=False,
    )

    parametres = construire_parametres_coupe(options)

    assert parametres["epaisseur_lame"] == attendu
    assert isinstance(parametres["epaisseur_lame"], int)


@pytest.mark.django_db
def test_construire_parametres_recupere_options_rotation_et_grain(
    projet_avec_panneau,
):
    options = OptionsDeCoupe.objects.create(
        projet=projet_avec_panneau,
        epaisseur_lame="5",
        rotation_autorisee=False,
        grain_strict=True,
    )

    parametres = construire_parametres_coupe(options)

    assert parametres["rotation_autorisee"] is False
    assert parametres["grain_strict"] is True