from django.urls import path
from .views import leaderboard_view, submit_score, leaderboard_view_following

app_name = 'leaderboards'
urlpatterns = [
    path('', leaderboard_view, name='leaderboard'),
    path('submit_score/', submit_score, name='submit'),
    path('following/<str:username>', leaderboard_view_following, name='following_leaderboard')
]