from .geometry import Rectangle

def decouper_zone(zone: Rectangle, largeur_piece: int, longueur_piece: int) -> list[Rectangle]:
    largeur_restante = zone.largeur - largeur_piece
    longueur_restante = zone.longueur - longueur_piece

    zones = []

    if largeur_restante > 0:
        zones.append(
            Rectangle(
                x=zone.x + largeur_piece,
                y=zone.y,
                largeur=largeur_restante,
                longueur=longueur_piece,
            )
        )

    if longueur_restante > 0:
        zones.append(
            Rectangle(
                x=zone.x,
                y=zone.y + longueur_piece,
                largeur=zone.largeur,
                longueur=longueur_restante,
            )
        )

    return zones

    