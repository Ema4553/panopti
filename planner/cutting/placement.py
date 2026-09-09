from dataclasses import dataclass
from .geometry import Rectangle, est_dans, se_chevauchent

@dataclass(frozen=True)
class Piece: 
    designation: str
    largeur: int
    longueur: int
    numero_exemplaire_piece: int = 1
    grain_direction: str | None = None

    def dimensions(self, retournee: bool = False) -> tuple[int, int]:
        if retournee:
            return self.longueur, self.largeur
        return self.largeur, self.longueur

@dataclass(frozen=True)
class CandidatPlacement:
    piece: Piece
    zone: Rectangle
    x: int
    y: int
    retournee: bool

    @property
    def largeur(self) -> int:
        return self.piece.dimensions(self.retournee)[0]

    @property
    def longueur(self) -> int:
        return self.piece.dimensions(self.retournee)[1]

    @property
    def surface_restante(self) -> int:
        return self.zone.surface - (self.largeur * self.longueur)



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


# Fonction qui vérifie si l'orientation choisie respecte bien le sens du grain
# Le panneau est considéré comme ayant son grain dans le sens de sa longueur
def orientation_respecte_grain(
        piece: Piece,
        retournee: bool,
        grain_strict: bool = False,
) -> bool:
    if not grain_strict:
        return True

    if piece.grain_direction is None:
        return True

    if piece.grain_direction == "length":
        return not retournee

    if piece.grain_direction == "width":
        return retournee

    return False


# Fonction qui fait une liste de toutes les pièces qui sont capables de rentrer dans la zone
def trouver_candidats(
        piece: Piece,
        zones_libres: list[Rectangle],
        placements_existants: list[Rectangle],
        rotation_autorisee: bool = True,
        epaisseur_lame: int = 0,
        grain_strict: bool = False
) -> list[CandidatPlacement]:
    candidats = []
    orientations = [False]

    if rotation_autorisee:
        orientations.append(True)

    for zone in zones_libres:
        for retournee in orientations:
            if not orientation_respecte_grain(
                piece=piece,
                retournee=retournee,
                grain_strict=grain_strict
            ):
                continue
            
            if not peut_etre_placee(
                piece=piece,
                panneau=zone,
                placements_existants=[],
                x=zone.x,
                y=zone.y,
                retournee=retournee
            ):
                continue

            candidats.append(
                CandidatPlacement(
                    piece=piece,
                    zone=zone,
                    x=zone.x,
                    y=zone.y,
                    retournee=retournee
                )
            )

    return candidats

# Fonction qui cherche la meilleure pièce à placer
def choisir_meilleur_candidat(candidats: list[CandidatPlacement]) -> CandidatPlacement | None:
    if not candidats:
        return None

    return min(candidats, key=lambda candidat: candidat.surface_restante)