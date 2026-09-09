from planner.cutting.optimizer import PanneauEnCours

# Fonction qui calcule la surface totale des pièces placées sur le panneau
def surface_pieces(panneau: PanneauEnCours) -> int:
    return sum(placement.largeur * placement.longueur for placement in panneau.placements)

# Fonction qui calcule la surface totale du panneau
def surface_panneau(panneau: PanneauEnCours) -> int:
    return panneau.rectangle.surface

# Fonction qui calcule la surface du panneau non occupée par les pièces
def surface_restante(panneau: PanneauEnCours) -> int:
    return surface_panneau(panneau) - surface_pieces(panneau)

# Fonction qui calcule le taux d'utilisation du panneau en pourcentage
def taux_utilisation(panneau: PanneauEnCours) -> float:
    surface = surface_panneau(panneau)

    if surface == 0:
        return 0.0

    return (surface_pieces(panneau) / surface) * 100

# Fonction qui calcule le taux de chute du panneau en pourcentage
def taux_chute(panneau: PanneauEnCours) -> float:
    return 100 - taux_utilisation(panneau)

# Fonction qui calcule le nombre de panneaux utilisés
def nombre_de_panneaux(panneaux: list[PanneauEnCours]) -> int:
    return len(panneaux)

# Fonction qui calcule la surface totale des panneaux utilisés
def surface_totale_panneaux(panneaux: list[PanneauEnCours]) -> int:
    return sum(surface_panneau(panneau) for panneau in panneaux)

# Fonction qui calcule la surface totale des pièces placées
def surface_totale_pieces(panneaux: list[PanneauEnCours]) -> int:
    return sum(surface_pieces(panneau) for panneau in panneaux)

# Fonction qui calcule le taux de chute global en pourcentage
def taux_chute_global(panneaux: list[PanneauEnCours]) -> float:
    surface_totale = surface_totale_panneaux(panneaux)

    if surface_totale == 0:
        return 0.0

    surface_pieces_total = surface_totale_pieces(panneaux)

    return ((surface_totale-surface_pieces_total) / surface_totale) * 100
