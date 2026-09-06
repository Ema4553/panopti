from django.shortcuts import render, redirect
from django.db import transaction

from .forms import (
    OptionsDeCoupeForm,
    PieceRequiseFormSet,
    ProjetForm,
)

from .models import PieceRequise

# ------------------------------------------------------------------------------------------------
# Définition de la fonction permettant de créer un projet avec le type de panneau utilisé, les pièces qui sont requises et les options de coupe qui ont été renseignés par l'utilisateur
def creer_projet(request):
    if request.method == "POST":
        projet_form = ProjetForm(request.POST)
        piece_formset = PieceRequiseFormSet(request.POST)
        options_form = OptionsDeCoupeForm(request.POST)

        if (projet_form.is_valid() and piece_formset.is_valid() and options_form.is_valid()):
            with transaction.atomic(): # transaction.atomic permet de faire une seule requête groupée avec les 3 formulaires, évite comme ça les erreurs qui auraient enregistré une partie des formulaires mais qui aurait crash avant la fin
                projet = projet_form.save()
                pieces = piece_formset.save(commit=False) # car le projet n'existe pas encore (clé étrangère) alors cela prépare les pièces mais ne les enregistre pas encore

                # Pour chaque pièce, attribue le projet qui vient d'être créé puis les enregistre
                for piece in pieces:
                    piece.projet = projet
                    piece.save()

                options = options_form.save(commit=False) # car le projet n'existe pas encore (clé étrangère) alors cela prépare les options mais ne les enregistre pas encore, comme pour les pièces
                options.projet = projet
                options.save()
            #return redirect("planner:detail_projet", projet_id=projet.id)    TODO : à remettre à la fin du test
            return redirect("planner:creer_projet")

    else:
        projet_form = ProjetForm()
        piece_formset = PieceRequiseFormSet(queryset=PieceRequise.objects.none())
        options_form = OptionsDeCoupeForm()

    context = {
        "projet_form": projet_form,
        "piece_formset": piece_formset,
        "options_form": options_form,
    }

    return render(request, "planner/creer_projet.html", context)