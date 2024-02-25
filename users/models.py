from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields like bio, profile picture, etc.
    bio = ''
    friends_list = []
    

    def __str__(self):
        return self.user.username


#friendship model represents an object that binds two users into friendship
class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name="friendship_creator_set", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="friend_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')