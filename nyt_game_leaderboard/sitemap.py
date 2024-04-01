from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from leaderboards.models import ConnectionsScore
from users.models import Profile

class CustomConnectionsScoreSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    #Define pattern for getting connections score
    def ConnectionsScore_items(self):
        return ConnectionsScore.objects.all()
    def location(self, item):
        return f"/connections_score/{item.pk}"