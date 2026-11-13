from decimal import Decimal
from django.db import transaction
from time import perf_counter

from planner.models import (
    ResultatDuCalcul,
    PanneauUtilise,
    Placement,
    PieceNonPlacee,
    Status,
)

from planner.services.calculation import calculer_decoupe

from planner.services.metrics import taux_utilisation


ALGORITHME_UTILISE = "First Fit Decreasing + Best Fit + Guillotine"


def sauvegarder_resultat_decoupe(
    projet,
    options,
    resultat,
    duree_ms: int,
) -> ResultatDuCalcul:
    """
    Enregistre un résultat de découpe et tous ses éléments associés.
    """

    if options.projet_id != projet.pk:
        raise ValueError(
            "Les options de coupe ne correspondent pas au projet."
        )

    # Vérification des références avant toute sauvegarde.
    toutes_les_pieces = [
        candidat.piece
        for panneau in resultat.panneaux
        for candidat in panneau.placements
    ] + resultat.pieces_non_placees

    if any(piece.piece_requise_id is None for piece in toutes_les_pieces):
        raise ValueError(
            "Une pièce ne possède pas de référence vers sa pièce requise."
        )

    statut = (
        Status.WARNING
        if resultat.pieces_non_placees
        else Status.SUCCESS
    )

    with transaction.atomic():

        resultat_db = ResultatDuCalcul.objects.create(
            projet=projet,
            options_coupe=options,
            duree_ms=duree_ms,
            statut=statut,
            nb_panneaux_utilises=resultat.nb_panneaux_utilises,
            taux_chute_global=Decimal(
                str(resultat.taux_chute_global)
            ).quantize(Decimal("0.01")),
            algorithme=ALGORITHME_UTILISE,
        )

        # Enregistrement des panneaux et de leurs placements.
        for numero, panneau in enumerate(resultat.panneaux, start=1):

            panneau_db = PanneauUtilise.objects.create(
                resultat_calcul=resultat_db,
                panneau_type=projet.panneau_type,
                numero_ordre=numero,
                taux_utilisation=Decimal(
                    str(taux_utilisation(panneau))
                ).quantize(Decimal("0.01")),
            )

            placements = []

            for candidat in panneau.placements:
                piece = candidat.piece

                placements.append(
                    Placement(
                        panneau_utilise=panneau_db,
                        piece_requise_id=piece.piece_requise_id,
                        numero_exemplaire_piece=(
                            piece.numero_exemplaire_piece
                        ),
                        x=candidat.x,
                        y=candidat.y,
                        largeur=candidat.largeur,
                        longueur=candidat.longueur,
                        est_retournee=candidat.retournee,
                    )
                )

            Placement.objects.bulk_create(placements)

        # Enregistrement des pièces qui n'ont pas pu être placées.
        pieces_non_placees = [
            PieceNonPlacee(
                resultat_calcul=resultat_db,
                piece_requise_id=piece.piece_requise_id,
                numero_exemplaire_piece=piece.numero_exemplaire_piece,
            )
            for piece in resultat.pieces_non_placees
        ]

        PieceNonPlacee.objects.bulk_create(pieces_non_placees)

    return resultat_db


def executer_et_sauvegarder_decoupe(projet, options):
    """
    Lance le calcul puis sauvegarde son résultat.
    """

    debut = perf_counter()

    resultat = calculer_decoupe(
        projet=projet,
        options=options,
    )

    duree_ms = round((perf_counter() - debut) * 1000)

    return sauvegarder_resultat_decoupe(
        projet=projet,
        options=options,
        resultat=resultat,
        duree_ms=duree_ms,
    )