from dataclasses import dataclass

@dataclass(frozen=True)
class Rectangle:
    x: int
    y: int
    largeur: int
    longueur: int

    @property
    def x_max(self) -> int:
        return self.x + self.largeur

    @property
    def y_max(self) -> int:
        return self.y + self.longueur

    @property
    def surface(self) -> int:
        return self.largeur * self.longueur

# Fonction qui teste si la pièce rentre dans le panneau et renvoit un booléen (true/false)
def est_dans(rectangle: Rectangle, contenant: Rectangle) -> bool:
    return (rectangle.x >= contenant.x
            and rectangle.y >= contenant.y
            and rectangle.x_max <= contenant.x_max
            and rectangle.y_max <= contenant.y_max)

# Fonction qui teste si deux pièces se chevauchent et renvoit un booléen (true/false)
def se_chevauchent(rectangle_a: Rectangle, rectangle_b: Rectangle) -> bool:
    return not (
        rectangle_a.x_max <= rectangle_b.x
        or rectangle_b.x_max <= rectangle_a.x
        or rectangle_a.y_max <= rectangle_b.y
        or rectangle_b.y_max <= rectangle_a.y
    )

# Fonction qui retourne les dimensions d'une pièce après rotation 
def dimensions_apres_rotation(largeur: int, longueur: int, retournee: bool) -> tuple[int, int]:
    if retournee:
        return longueur, largeur
    return largeur, longueur