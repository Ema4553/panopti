from .geometry import Rectangle

def decouper_zone(zone: Rectangle, largeur_piece: int, longueur_piece: int, epaisseur_lame: int = 0) -> list[Rectangle]:
    largeur_restante = zone.largeur - largeur_piece
    longueur_restante = zone.longueur - longueur_piece

    zones = []

    # Le trait de scie est retiré horizontalement entre la pièce et la zone à sa droite
    largeur_zone_droite = largeur_restante - epaisseur_lame

    if largeur_zone_droite > 0:
        zones.append(
            Rectangle(
                x=zone.x + largeur_piece + epaisseur_lame,
                y=zone.y,
                largeur=largeur_zone_droite,
                longueur=longueur_piece,
            )
        )

    # Le trait de scie est retiré verticalement entre la pièce et la zone en dessous
    longueur_zone_bas = longueur_restante - epaisseur_lame

    if longueur_zone_bas > 0:
        zones.append(
            Rectangle(
                x=zone.x,
                y=zone.y + longueur_piece + epaisseur_lame,
                largeur=zone.largeur,
                longueur=longueur_zone_bas,
            )
        )

    return zones

    