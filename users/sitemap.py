from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from users.models import Profile

class ProfileListSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        # Return a list of genres to create a URL for each genre filter
        return Profile.objects.all()

    def location(self, item):
        genre = item[0]  # item is a tuple (value, verbose_name)
        return reverse('podcast-list') + f'?genre={genre}'
