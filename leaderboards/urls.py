from django.urls import path
from .views import leaderboard_view, submit_score

app_name = 'leaderboards'
urlpatterns = [
    path('', leaderboard_view, name='leaderboard'),
    path('submit_score/', submit_score, name='submit')
]