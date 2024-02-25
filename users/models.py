from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields like bio, profile picture, etc.
    bio = ''
    
    #many-to-many field to track many freinds 
    #friends = models.ManyToManyField('self', blank=True)

    #gets all the names of friends in the realtionships 
    def get_friends_profiles_following(self):
        # Assuming 'Friendship' is the name of the model representing the relationship
        # This will fetch all users where the current user is the 'from_user'
        friendships = Friendship.objects.filter(from_user=self.user)
        friend_user_ids = friendships.values_list('to_user_id', flat=True)
        # Return profiles of these friends
        return Profile.objects.filter(user_id__in=friend_user_ids)

    def get_friends_profiles_followers(self):
        # Assuming 'Friendship' is the name of the model representing the relationship
        # This will fetch all users where the current user is the 'from_user'
        friendships = Friendship.objects.filter(to_user=self.user)
        friend_user_ids = friendships.values_list('from_user_id', flat=True)
        # Return profiles of these friends
        return Profile.objects.filter(user_id__in=friend_user_ids)


    def __str__(self):
        return self.user.username


#friendship model represents an object that binds two users into friendship
class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name="friendship_creator_set", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="friend_set", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')