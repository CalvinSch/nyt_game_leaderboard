from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout #built in funcitons from django
from .models import Profile, Friendship

from django.db.models import Q

from django.contrib.auth.models import User
from django.db import IntegrityError

##skearns, seanpjk@gmail.com, bigredcat

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login_view"))
    #return render(request, "users/user.html")
    return redirect(reverse("leaderboards:leaderboard"))
    
def login_view(request):
    if request.method =='POST':
        username = request.POST['username'] #request object contains info from the form that is submitted 
        password = request.POST['password']

        user = authenticate(request, username=username, password=password) #function that takes the request and passes a username and password and returns a user if there is one 
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid Credentials."
            })

    context = {'login_view': login_view}
    return render(request, "users/login.html")
    #return redirect(reverse("users:login"))
    #return HttpResponseRedirect(reverse("users:login"))

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out."
    })


#user profile view, renders the profile html page 
def user_profile_view(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)

    user = get_object_or_404(User, username=username)

    # Get the list of friends' profiles
    friends_profiles_following = user_profile.get_friends_profiles_following()
    friends_profiles_followers = user_profile.get_friends_profiles_followers()

    # # Fetch friendships where the user is either the 'from_user' or 'to_user'
    # friendships = Friendship.objects.filter(Q(from_user=user) | Q(to_user=user))

    # # Preparing a list of friends' profiles
    # friends_profiles = []
    # for friendship in friendships:
    #     # Add the other user's profile to the list
    #     friend_profile = friendship.to_user.profile if friendship.from_user == user else friendship.from_user.profile
    #     friends_profiles.append(friend_profile)


    return render(request, 'users/profile.html', 
            {'profile': user_profile, 
            'user': user, 
            'friends_profiles_following': friends_profiles_following,
            'friends_profiles_followers': friends_profiles_followers})


# def add_friend_view(request, user_id):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             user_to_add = get_object_or_404(User, pk=user_id)
#             if request.user != user_to_add:
#                 try:
#                     # Attempt to create the friendship
#                     Friendship.objects.create(from_user=request.user, to_user=user_to_add)
        
#                     #returning the user_profile url with an argument so it finds the right page 
#                     return redirect(reverse('users:user_profile', kwargs={'username': request.user.username}))  # Redirect to an appropriate page
#                     #'profile', username=user.username
#                 except IntegrityError:
#                     # Handle the case where the friendship already exists
#                     return HttpResponse("Friendship already exists.")
#             else:
#                 return HttpResponse("You cannot add yourself as a friend.")
#         else:
#             return HttpResponse("You must be logged in to add friends.")
#     else:
#         return HttpResponse("Invalid request.")


def add_friend_view(request, user_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            user_to_add = get_object_or_404(User, pk=user_id)
            if request.user != user_to_add:
                try:
                    # Attempt to create the friendship
                    Friendship.objects.create(from_user=request.user, to_user=user_to_add)

                    # Add a success message
                    messages.success(request, "Friend successfully added!")

                except IntegrityError:
                    # Handle the case where the friendship already exists
                    messages.error(request, "You are great friends with this person already!")
                    return redirect(reverse('users:list_users'))

            else:
                messages.error(request, "You cannot add yourself as a friend, silly goose.")
                return redirect(reverse('users:list_users'))
        else:
            messages.error(request, "You must be logged in to add friends.")
            return redirect(reverse('users:list_users'))
    else:
        messages.error(request, "Invalid request.")
        return redirect(reverse('users:list_users'))

    # Redirect back to the same page or another page of your choice
    return redirect(reverse('users:user_profile', kwargs={'username': request.user.username}))  # Redirect to an appropriate page


def list_users_view(request):
    users = User.objects.all()
    return render(request, 'users/list_users.html', {'users': users})


def delete_relationship_view(request, friend_id):
    if request.method == "POST":
        # Assume the user initiating the request is the 'from_user'
        relationship = get_object_or_404(Friendship, from_user=request.user, to_user_id=friend_id)
        relationship.delete()
        messages.success(request, "Friendship removed successfully.")
    return redirect(reverse('users:user_profile', kwargs={'username': request.user.username})) 