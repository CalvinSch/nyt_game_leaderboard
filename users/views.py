from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout #built in funcitons from django
from .models import Profile

from django.contrib.auth.models import User

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
    user_profile = Profile.objects.get(user__username=username)
    return render(request, 'users/profile.html', {'profile': user_profile})


##making views for users to add friends by searching for them 
def add_friend_view(request, user_id):
    user_to_add = User.objects.get(pk=user_id)
    Friendship.objects.create(from_user=request.user, to_user=user_to_add)
    return HttpResponseRedirect('/wherever-you-want-to-redirect')

def list_users_view(request):
    users = User.objects.all()
    return render(request, 'users/list_users.html', {'users': users})