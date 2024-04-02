from django.urls import path 
from django.urls import include, path
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from .sitemap import ProfileListSitemap


from users.views import (index, login_view, logout_view, user_profile_view, add_friend_view, list_users_view, delete_relationship_view, register_view,
followers_list_view, following_list_view, badge_list_view, set_username_view, edit_bio_view)
from users.models import Profile
from leaderboards.views import leaderboard_view, submit_score
from . import views

# #url patterns from google SSO tutorial 
# urlpatterns = [
#     path("", views.home),
#     path("logout", views.logout_view)
# ]

#Define Sitemaps Dict to point to ProfileListSitemap
sitemaps = {
    'profiles': ProfileListSitemap,
}

app_name = 'users'
urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name='login'),
    path('register', register_view, name='register'),
    path("logout", logout_view, name='logout'),
    path("set_username", set_username_view, name="set_username"),
    #path('leaderboards/', leaderboard_view, name='leaderboard_view'),
    ##individual user profile page 
    path('<str:username>', user_profile_view, name='user_profile'),

    path('edit_bio/<str:username>', edit_bio_view, name='edit_bio'),
    
    path('badges/<str:username>', badge_list_view, name='badge_list'),
    path('following_list/<str:username>', following_list_view, name='following_list'),
    path('followers_list/<str:username>', followers_list_view, name='followers_list'),
    #path to add as a friend
    path('add_friend/<int:user_id>/', add_friend_view, name='add_friend'),
    #path to list all users so that people can add them as friends 
    path('list_users/', list_users_view, name='list_users'),
    path('delete_relationship/<int:friend_id>/', delete_relationship_view, name='delete_relationship'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    #Sitemap URL Path
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
]
