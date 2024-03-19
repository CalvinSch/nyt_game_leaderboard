from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import redirect


#ths is used to make a profile everything a new user is created!
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    # Check if the user signed up via Google
    sociallogin = kwargs.get('sociallogin')
    if sociallogin and sociallogin.account.provider == 'google':
        # Set a flag on the session or redirect to username set page
        request.session['user_needs_username'] = True
        # Redirect to set username page
        return redirect('set_username_url')  # Make sure to replace 'set_username_url' with your actual URL name