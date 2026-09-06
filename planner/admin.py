from django.contrib import admin

# Importer les modèles pour avoir une interface de contrôle temporaire
from .models import (
    PanneauType,
    Projet,
    PieceRequise,
    OptionsDeCoupe,
    ResultatDuCalcul,
    PanneauUtilise,
    Placement,
)

admin.site.register(PanneauType)
admin.site.register(Projet)
admin.site.register(PieceRequise)
admin.site.register(OptionsDeCoupe)
admin.site.register(ResultatDuCalcul)
admin.site.register(PanneauUtilise)
admin.site.register(Placement)