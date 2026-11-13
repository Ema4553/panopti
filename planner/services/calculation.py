from dataclasses import dataclass
from planner.models import Projet, OptionsDeCoupe
from planner.cutting.placement import Piece
from planner.cutting.geometry import Rectangle
from planner.cutting.optimizer import (
    optimiser_decoupe,
    ResultatOptimisation,
    PanneauEnCours
)
from planner.services.metrics import (
    nombre_de_panneaux,
    surface_totale_panneaux,
    surface_totale_pieces,
    taux_chute_global,
)


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


@dataclass
class ResultatDecoupe:
    panneaux: list[PanneauEnCours]
    pieces_non_placees: list[Piece]
    nb_panneaux_utilises: int
    surface_totale_panneaux: int
    surface_pieces_placees: int
    taux_chute_global: float


def calculer_decoupe(
    projet: Projet,
    options: OptionsDeCoupe,
) -> ResultatDecoupe:

    if options.projet_id != projet.pk:
        raise ValueError(
            "Les options de coupe ne correspondent pas au projet."
        )

    pieces = construire_pieces(projet)
    panneau = construire_panneau(projet)
    parametres = construire_parametres_coupe(options)

    optimisation = optimiser_decoupe(
        pieces=pieces,
        panneau=panneau,
        **parametres,
    )

    panneaux = optimisation.panneaux

    return ResultatDecoupe(
        panneaux=panneaux,
        pieces_non_placees=optimisation.pieces_non_placees,
        nb_panneaux_utilises=nombre_de_panneaux(panneaux),
        surface_totale_panneaux=surface_totale_panneaux(panneaux),
        surface_pieces_placees=surface_totale_pieces(panneaux),
        taux_chute_global=taux_chute_global(panneaux),
    )