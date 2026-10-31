from dataclasses import dataclass

from .geometry import Rectangle
from .guillotine import decouper_zone
from .placement import (
    CandidatPlacement,
    Piece,
    choisir_meilleur_candidat,
    trouver_candidats
)

@dataclass
class PanneauEnCours:
    rectangle: Rectangle
    zones_libres: list[Rectangle]
    placements: list[CandidatPlacement]

@dataclass
class ResultatOptimisation:
    panneaux: list[PanneauEnCours]
    pieces_non_placees: list[Piece]


# Fonction qui trie les pièces par surface décroissante
def trier_pieces(pieces: list[Piece]) -> list[Piece]:
    return sorted(
        pieces,
        key=lambda piece: piece.largeur * piece.longueur,
        reverse=True
    )


# Fonction qui créé un panneau vide avec l'entièreté de sa surface vide
def creer_panneau(rectangle: Rectangle) -> PanneauEnCours:
    return PanneauEnCours(
        rectangle=rectangle,
        zones_libres=[rectangle],
        placements=[]
    )


# Fonction qui place une pièce dans un panneau et qui met à jour les zones libres
def appliquer_placement(panneau: PanneauEnCours, candidat: CandidatPlacement, epaisseur_lame: int = 0) -> None:
    panneau.zones_libres.remove(candidat.zone)

    nouvelles_zones = decouper_zone(
        zone=candidat.zone,
        largeur_piece=candidat.largeur,
        longueur_piece=candidat.longueur,
        epaisseur_lame=epaisseur_lame
    )

    panneau.zones_libres.extend(nouvelles_zones)
    panneau.placements.append(candidat)


# Fonction qui optimise le nombre de panneaux utilisés en utilisant au mieux les zones dispo (stratégie de First Fit Decreasing & découpe guillotine)
def optimiser_decoupe(
        pieces: list[Piece],
        panneau: Rectangle,
        rotation_autorisee: bool = True,
        epaisseur_lame: int = 0,
        grain_strict: bool = False
) -> ResultatOptimisation:
    panneaux: list[PanneauEnCours] = []
    pieces_non_placees: list[Piece] = []
    pieces_triees = trier_pieces(pieces)

    for piece in pieces_triees:
        piece_placee = False

        # étape 1 : tester les panneaux déjà existants
        for panneau_en_cours in panneaux:
            candidats = trouver_candidats(
                piece=piece,
                zones_libres=panneau_en_cours.zones_libres,
                rotation_autorisee=rotation_autorisee,
                grain_strict=grain_strict
            )

            candidat = choisir_meilleur_candidat(candidats)

            if candidat is None:
                continue

            appliquer_placement(
                panneau=panneau_en_cours,
                candidat=candidat,
                epaisseur_lame=epaisseur_lame
            )

            piece_placee = True
            break

        if piece_placee:
            continue

        # étape 2 : tester un panneau vide 
        nouveau_panneau = creer_panneau(panneau)

        candidats = trouver_candidats(
            piece=piece,
            zones_libres=nouveau_panneau.zones_libres,
            rotation_autorisee=rotation_autorisee,
            grain_strict=grain_strict
        )

        candidat = choisir_meilleur_candidat(candidats)

        # étape 3 : la pièce ne rentre pas, peut importe si le panneau est nouveau ou pas
        if candidat is None:
            pieces_non_placees.append(piece)
            continue

        appliquer_placement(
            panneau=nouveau_panneau,
            candidat=candidat,
            epaisseur_lame=epaisseur_lame
        )

        panneaux.append(nouveau_panneau)

    return ResultatOptimisation(
        panneaux=panneaux,
        pieces_non_placees=pieces_non_placees
    )