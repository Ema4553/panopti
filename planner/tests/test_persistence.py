import pytest

from unittest.mock import patch

from planner.models import (
    PieceRequise,
    OptionsDeCoupe,
    ResultatDuCalcul,
    PanneauUtilise,
    Placement,
    PieceNonPlacee,
    Status,
)

from planner.services.persistence import (
    executer_et_sauvegarder_decoupe,
)

## Test qui vérifie toute la chaine : résultat, panneau, placements et absence d'avertissements
@pytest.mark.django_db
def test_sauvegarder_decoupe_enregistre_resultat_complet(
    projet_avec_panneau,
):
    projet = projet_avec_panneau

    piece_requise = PieceRequise.objects.create(
        projet=projet,
        designation="Côté",
        longueur=600,
        largeur=400,
        epaisseur=18,
        quantite=2,
    )

    options = OptionsDeCoupe.objects.create(
        projet=projet,
        epaisseur_lame="5",
        rotation_autorisee=True,
        grain_strict=False,
    )

    resultat = executer_et_sauvegarder_decoupe(
        projet=projet,
        options=options,
    )

    # Vérification du résultat global
    assert isinstance(resultat, ResultatDuCalcul)
    assert resultat.projet == projet
    assert resultat.options_coupe == options
    assert resultat.statut == Status.SUCCESS
    assert resultat.nb_panneaux_utilises == 1
    assert resultat.duree_ms >= 0

    # Vérification des panneaux
    panneaux = PanneauUtilise.objects.filter(
        resultat_calcul=resultat
    )

    assert panneaux.count() == 1

    panneau = panneaux.first()

    assert panneau.numero_ordre == 1
    assert panneau.panneau_type == projet.panneau_type

    # Vérification des placements
    placements = Placement.objects.filter(
        panneau_utilise__resultat_calcul=resultat
    )

    assert placements.count() == 2

    assert all(
        placement.piece_requise == piece_requise
        for placement in placements
    )

    assert sorted(
        placement.numero_exemplaire_piece
        for placement in placements
    ) == [1, 2]

    # Vérification des pièces non placées
    assert PieceNonPlacee.objects.filter(
        resultat_calcul=resultat
    ).count() == 0


## Test qui vérifie quand une pièce ne peut pas respecter sa direction de grain sans rotation, avec rotation interdite : la pièce doit donc être laissée de côté sans faire échouer le test
@pytest.mark.django_db
def test_sauvegarder_decoupe_enregistre_pieces_non_placees(
    projet_avec_panneau,
):
    projet = projet_avec_panneau

    piece_requise = PieceRequise.objects.create(
        projet=projet,
        designation="Façade",
        longueur=600,
        largeur=400,
        epaisseur=18,
        quantite=1,
        grain_direction="width",
    )

    options = OptionsDeCoupe.objects.create(
        projet=projet,
        epaisseur_lame="5",
        rotation_autorisee=False,
        grain_strict=True,
    )

    resultat = executer_et_sauvegarder_decoupe(
        projet=projet,
        options=options,
    )

    # Le calcul s'est terminé, mais avec un avertissement.
    assert resultat.statut == Status.WARNING

    # Aucun panneau n'a été utilisé.
    assert resultat.nb_panneaux_utilises == 0

    assert PanneauUtilise.objects.filter(
        resultat_calcul=resultat
    ).count() == 0

    assert Placement.objects.filter(
        panneau_utilise__resultat_calcul=resultat
    ).count() == 0

    # La pièce non placée est bien conservée.
    pieces_non_placees = PieceNonPlacee.objects.filter(
        resultat_calcul=resultat
    )

    assert pieces_non_placees.count() == 1

    piece_non_placee = pieces_non_placees.first()

    assert piece_non_placee.piece_requise == piece_requise
    assert piece_non_placee.numero_exemplaire_piece == 1


## Test qui simule une erreur juste après la création du résultat : la transaction annule donc le résultat créé
@pytest.mark.django_db
def test_sauvegarde_annulee_si_erreur_pendant_creation_panneau(
    projet_avec_panneau,
):
    projet = projet_avec_panneau

    PieceRequise.objects.create(
        projet=projet,
        designation="Côté",
        longueur=600,
        largeur=400,
        epaisseur=18,
        quantite=1,
    )

    options = OptionsDeCoupe.objects.create(
        projet=projet,
        epaisseur_lame="5",
        rotation_autorisee=True,
        grain_strict=False,
    )

    with patch(
        "planner.services.persistence.PanneauUtilise.objects.create",
        side_effect=RuntimeError("Erreur simulée"),
    ):
        with pytest.raises(RuntimeError, match="Erreur simulée"):
            executer_et_sauvegarder_decoupe(
                projet=projet,
                options=options,
            )

    # Le résultat créé avant l'erreur doit avoir été annulé.
    assert ResultatDuCalcul.objects.count() == 0

    # Aucun panneau ne doit avoir été conservé.
    assert PanneauUtilise.objects.count() == 0

    # Aucun placement ne doit avoir été conservé.
    assert Placement.objects.count() == 0