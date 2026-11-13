import uuid

from django.db import models


# ------------------------------------------------------------------------------------------------
# Définition de la classe d'un panneau type (id, nom, longueur, largeur, épaisseur)
class PanneauType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    nom = models.CharField(max_length=100)
    longueur = models.PositiveIntegerField()
    largeur = models.PositiveIntegerField()
    epaisseur = models.PositiveIntegerField()

    def __str__(self):
        return self.nom


# ------------------------------------------------------------------------------------------------
# Définition de la classe d'un projet (id, nom, description, id du panneau type, date de création du projet)
class Projet(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    panneau_type = models.ForeignKey(
        PanneauType,
        on_delete=models.PROTECT,
        related_name="projets"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


# ------------------------------------------------------------------------------------------------
# Définition de l'ENUM pour la direction du grain, utilisé dans les pièces requises
class GrainDirection(models.TextChoices):
    LENGTH = "length", "Longueur"
    WIDTH = "width", "Largeur"


# ------------------------------------------------------------------------------------------------
# Définition de la classe des pièces qui doivent être fabriquées (id, id du projet, désignation ou nom, longueur, largeur, épaisseur, quantité, direction du grain)
class PieceRequise(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name="pieces_requises"
    )

    designation = models.CharField(max_length=255)
    longueur = models.PositiveIntegerField()
    largeur = models.PositiveIntegerField()
    epaisseur = models.PositiveIntegerField()
    quantite = models.PositiveIntegerField()

    grain_direction = models.CharField(
        max_length=6,
        choices=GrainDirection.choices,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.designation


# ------------------------------------------------------------------------------------------------
# Définition de l'ENUM pour l'épaisseur de la lame (3 ou 5mm)
class Kerf(models.TextChoices):
    MM_3 = "3", "3mm"
    MM_5 = "5", "5mm"


# ------------------------------------------------------------------------------------------------
# Définition de la classe des options de coupe (id, id du projet, épaisseur de la lame, rotation autorisée, grain spécifique)
class OptionsDeCoupe(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name="options_de_coupe"
    )

    epaisseur_lame = models.CharField(
        max_length=1,
        choices=Kerf.choices,
        default="5"
    )

    rotation_autorisee = models.BooleanField(default=True)
    grain_strict = models.BooleanField(default=False)

    def __str__(self):
        return f"Options de coupe - {self.projet.nom}"


# ------------------------------------------------------------------------------------------------
# Définition de l'ENUM du statut (en attente, réussi, erreur)
class Status(models.TextChoices):
    PENDING = "pending", "En attente"
    SUCCESS = "success", "Réussi"
    WARNING = "warning", "Terminé avec avertissements"
    ERROR = "error", "Erreur"


# ------------------------------------------------------------------------------------------------
# Définition du résultat de calcul (id, id du projet, id de l'option de coupe, date du calcul, durée du calcul en ms, statut, nb de panneaux utilisés, algorithme utilisé)
class ResultatDuCalcul(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name="resultats"
    )

    options_coupe = models.ForeignKey(
        OptionsDeCoupe,
        on_delete=models.PROTECT,
        related_name="resultats"
    )

    calcule_le = models.DateTimeField(auto_now_add=True)
    duree_ms = models.PositiveIntegerField()

    statut = models.CharField(
        max_length=10,
        choices=Status.choices
    )

    nb_panneaux_utilises = models.PositiveIntegerField()
    taux_chute_global = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    algorithme = models.TextField()

    def __str__(self):
        return f"Calcul du {self.calcule_le}"


# ------------------------------------------------------------------------------------------------
# Définition de la classe du panneau utilisé (id, id du résultat du calcul, id du panneau type, numéro, taux d'utilisation)
class PanneauUtilise(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resultat_calcul = models.ForeignKey(
        ResultatDuCalcul,
        on_delete=models.CASCADE,
        related_name="panneaux_utilises"
    )

    panneau_type = models.ForeignKey(
        PanneauType,
        on_delete=models.PROTECT,
        related_name="utilisations"
    )

    numero_ordre = models.PositiveIntegerField()

    taux_utilisation = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return f"Panneau {self.numero_ordre}"


# ------------------------------------------------------------------------------------------------
# Définition de la classe du placement (id, id du panneau utilisé, id des pièces, numéro de l'exemplaire de la pièce, x, y, largeur, longueur, est retournée)
class Placement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    panneau_utilise = models.ForeignKey(
        PanneauUtilise,
        on_delete=models.CASCADE,
        related_name="placements"
    )

    piece_requise = models.ForeignKey(
        PieceRequise,
        on_delete=models.PROTECT,
        related_name="placements"
    )

    numero_exemplaire_piece = models.PositiveIntegerField()

    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()

    longueur = models.PositiveIntegerField()
    largeur = models.PositiveIntegerField()

    est_retournee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.piece_requise.designation} #{self.numero_exemplaire_piece}"


# ------------------------------------------------------------------------------------------------
# Définition des pièces qui n'ont pas pu être placées lors d'un calcul
class PieceNonPlacee(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resultat_calcul = models.ForeignKey(
        ResultatDuCalcul,
        on_delete=models.CASCADE,
        related_name="pieces_non_placees"
    )

    piece_requise = models.ForeignKey(
        PieceRequise,
        on_delete=models.PROTECT,
        related_name="pieces_non_placees"
    )

    numero_exemplaire_piece = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"{self.piece_requise.designation} "
            f"#{self.numero_exemplaire_piece} non placée"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "resultat_calcul",
                    "piece_requise",
                    "numero_exemplaire_piece",
                ],
                name="unique_piece_non_placee_par_calcul",
            )
        ]