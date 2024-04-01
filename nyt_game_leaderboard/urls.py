"""
URL configuration for nyt_game_leaderboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from .sitemap import CustomConnectionsScoreSitemap

#Models for sitemapping
from users.models import Profile
from leaderboards.models import ConnectionsScore

# #Example url_patterns from video 
# urlpatterns = [
#     path('', include("googleauthentication.urls")),
#     path('accounts/', include("allauth.urls")),
#     path('admin/', admin.site.urls),
#     path("/", include(users.urls))
# ]


#SEO Dictionary of users and scores to help with sitemapping. NEEDS queryset entry
info_dict_queryset = {
    #If we pass in these dictionaries, search engines can navigate through profiles and scores
    #"profile_queryset": Profile.objects.all(),
    "queryset": ConnectionsScore.objects.all(),
    "date_field": "date",
}

urlpatterns = [
    path('', include("leaderboards.urls"), name='leaderboard'), 
    path('accounts/', include("allauth.urls")),
    path('accounts/', include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    #Sitemap (Keep Last, update info dictionary as needed)
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"leaderboard": CustomConnectionsScoreSitemap()}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
