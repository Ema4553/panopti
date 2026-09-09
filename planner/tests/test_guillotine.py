from planner.cutting.geometry import Rectangle
from planner.cutting.guillotine import decouper_zone

# Fonction qui teste si la pièce placée créé bien deux zones
def test_decoupe_zone_en_deux():
    zone = Rectangle(
        x=0,
        y=0,
        largeur=2800,
        longueur=2070,
    )

    zones = decouper_zone(
        zone=zone,
        largeur_piece=800,
        longueur_piece=400,
    )

    assert len(zones) == 2

    zone_droite = zones[0]

    assert zone_droite.x == 800
    assert zone_droite.y == 0
    assert zone_droite.largeur == 2000
    assert zone_droite.longueur == 400

    zone_dessous = zones[1]

    assert zone_dessous.x == 0
    assert zone_dessous.y == 400
    assert zone_dessous.largeur == 2800
    assert zone_dessous.longueur == 1670

# Fonction qui teste le cas où la pièce fait la taille de la zone restante
def test_decoupe_exacte_ne_cree_pas_de_zone_vide():
    zone = Rectangle(
        x=0,
        y=0,
        largeur=800,
        longueur=400,
    )

    zones = decouper_zone(
        zone=zone,
        largeur_piece=800,
        longueur_piece=400,
    )

    assert zones == []

# Fonction qui teste la découpe avec une épaisseur de lame
def test_decouper_zone_avec_kerf():
    zone = Rectangle(
        x=0,
        y=0,
        largeur=1000,
        longueur=1000,
    )

    zones = decouper_zone(
        zone=zone,
        largeur_piece=600,
        longueur_piece=600,
        epaisseur_lame=5,
    )

    assert zones == [
        Rectangle(
            x=605,
            y=0,
            largeur=395,
            longueur=600,
        ),
        Rectangle(
            x=0,
            y=605,
            largeur=1000,
            longueur=395,
        ),
    ]