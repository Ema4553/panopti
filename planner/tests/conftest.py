import pytest

from planner.models import Projet, PanneauType


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