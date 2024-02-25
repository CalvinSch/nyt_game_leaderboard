from django.urls import path 


from users.views import index, login_view, logout_view, user_profile_view, add_friend_view, list_users_view
from leaderboards.views import leaderboard_view, submit_score
from . import views


app_name = 'users'
urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name='login'),
    path("logout", logout_view, name='logout'),
    #path('leaderboards/', leaderboard_view, name='leaderboard_view'),
    ##individual user profile page 
    #path('users/<str:username>/', user_profile_view, name='user_profile'),
    path('<str:username>', user_profile_view, name='user_profile'),
    #path to add as a friend
    path('add_friend/<int:user_id>/', add_friend_view, name='add_friend'),
    #path to list all users so that people can add them as friends 
    path('list_users/', list_users_view, name='list_users'),
]
