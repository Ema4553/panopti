from planner.models import Projet, OptionsDeCoupe
from planner.cutting.placement import Piece
from planner.cutting.geometry import Rectangle

def construire_pieces(projet: Projet) -> list[Piece]:
    pieces = []
    pieces_requises = projet.pieces_requises.all()

    for piece_requise in pieces_requises:
        for numero in range(1, piece_requise.quantite + 1):
            pieces.append(
                Piece(
                    designation=piece_requise.designation,
                    largeur=piece_requise.largeur,
                    longueur=piece_requise.longueur,
                    numero_exemplaire_piece=numero,
                    grain_direction=piece_requise.grain_direction,
                )
            )

    return pieces


def construire_panneau(projet: Projet) -> Rectangle:
    panneau_type = projet.panneau_type

    return Rectangle(
        x=0,
        y=0,
        largeur=panneau_type.largeur,
        longueur=panneau_type.longueur,
    )


def construire_parametres_coupe(
    options: OptionsDeCoupe,
) -> dict[str, int | bool]:
    return {
        "epaisseur_lame": int(options.epaisseur_lame),
        "rotation_autorisee": options.rotation_autorisee,
        "grain_strict": options.grain_strict,
    }