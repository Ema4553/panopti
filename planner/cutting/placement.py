from dataclasses import dataclass
from .geometry import Rectangle, est_dans, se_chevauchent

@dataclass(frozen=True)
class Piece: 
    designation: str
    largeur: int
    longueur: int
    numero_exemplaire_piece: int = 1

    def dimensions(self, retournee: bool = False) -> tuple[int, int]:
        if retournee:
            return self.longueur, self.largeur
        return self.largeur, self.longueur


def peut_etre_placee(piece: Piece, panneau: Rectangle, placements_existants: list[Rectangle], x: int, y: int, retournee: bool = False) -> bool:
    largeur, longueur = piece.dimensions(retournee)

    rectangle_piece = Rectangle(
        x=x, 
        y=y,
        largeur=largeur,
        longueur=longueur,
    )

    if not est_dans(rectangle_piece, panneau):
        return False

    for placement in placements_existants:
        if se_chevauchent(rectangle_piece, placement):
            return False

    return True