from django.urls import path
from .views import leaderboard_view, submit_score

urlpatterns = [
    path('', leaderboard_view, name='leaderboard'),
    path('submit_score/', submit_score, name='submit')
]