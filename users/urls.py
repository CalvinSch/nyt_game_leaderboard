from django.urls import path 


from users.views import index, login_view, logout_view 
from leaderboards.views import leaderboard_view, submit_score


app_name = 'users'
urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name='login'),
    path("logout", logout_view, name='logout'),
    path('leaderboards/', leaderboard_view, name='leaderboard_view'),
]