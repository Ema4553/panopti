from django import forms
from django.forms import modelformset_factory

from .models import (
    Projet,
    PieceRequise,
    OptionsDeCoupe,
)

# ------------------------------------------------------------------------------------------------
# Définition du formulaire de création d'un projet
class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = [
            "nom",
            "description",
            "panneau_type",
        ]

        labels = {
            "nom": "Nom du projet",
            "description": "Description",
            "panneau_type": "Type de panneau",
        }

        widget = {
            "nom": forms.TextInput(attrs={
                "placeholder": "Ex. Meuble de cuisine de Fred"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Description du projet",
                "rows": 4,
            }),
            "panneau_type": forms.Select(),
        }


# ------------------------------------------------------------------------------------------------
# Définition du formulaire de création d'une pièce à fabriquer
class PieceRequiseForm(forms.ModelForm):
    class Meta:
        model = PieceRequise
        fields = [
            "designation",
            "longueur",
            "largeur",
            'epaisseur',
            "quantite",
            "grain_direction",
        ]

        labels = {
            "designation": "Désignation",
            "longueur": "Longueur",
            "largeur": "Largeur",
            "epaisseur": "Épaisseur",
            "quantite": "Quantité",
            "grain_direction": "Sens du fil",
        }


# ------------------------------------------------------------------------------------------------
# Définition du formulaire de création d'une option de coupe
class OptionsDeCoupeForm(forms.ModelForm):
    class Meta:
        model = OptionsDeCoupe
        fields = [
            "epaisseur_lame",
            "rotation_autorisee",
            "grain_strict",
        ]

        labels = {
            "epaisseur_lame": "Épaisseur de lame",
            "rotation_autorisee": "Rotation autorisée",
            "grain_strict": "Respect strict du grain",
        }


# ------------------------------------------------------------------------------------------------
PieceRequiseFormSet = modelformset_factory(
    PieceRequise,
    form=PieceRequiseForm,
    extra=1,
    can_delete=True,
)