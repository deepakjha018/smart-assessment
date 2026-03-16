from django.urls import path
from .views import dashboard_home, leaderboard

urlpatterns = [
    path("", dashboard_home, name="dashboard"),
    path("leaderboard/", leaderboard, name="leaderboard"),
]