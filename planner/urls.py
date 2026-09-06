from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    path(
        "nouveau-projet/",
        views.creer_projet,
        name="creer_projet",
    ),
]