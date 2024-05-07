##web handling
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

##user creation and authentication 
from django.contrib.auth import authenticate, login, logout #built in funcitons from django
from django.contrib.auth.forms import UserCreationForm

##models 
from .models import Profile, Friendship
from django.contrib.auth.models import User
from leaderboards.models import ConnectionsScore
from django.db.models import Q, Avg #querying models and mods

from collections import Counter
import json
from django.core.serializers import serialize

#error handling 
from django.db import IntegrityError

#for API - used pip install djangorestframework
from rest_framework.views import APIView
from rest_framework.response import Response



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


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Log the user in (optional)
            login(request, user)

            # Redirect to the user's profile page
            return redirect('users:user_profile', username=user.username)
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


##this view will be used after a user authenitcates with google so that they can still make a username 
def set_username_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            request.user.username = username
            request.user.save()
            del request.session['user_needs_username']
            return redirect(reverse('users:list_users'))  # Redirect to desired URL after setting username
    return render(request, 'set_username.html')


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged out."
    })




#user profile view, renders the profile html page 
##this view also pulls alot of the important information related to the user object by calling methods of Profile
def user_profile_view(request, username):
    #Need immediate handler for no users, redirect to registration?
    if username == '':
        return redirect(reverse('users:register_view'))

    #obtain the instance of the profile and user based on the username on the page 
    user_profile = get_object_or_404(Profile, user__username=username)
    user = get_object_or_404(User, username=username)

    # Get the list of friends' profiles from the profile object method called get_friends_profiles_following/followers
    #also get badges and bio 
    friends_profiles_following = user_profile.get_friends_profiles_following()
    friends_profiles_followers = user_profile.get_friends_profiles_followers()
    badges = user_profile.get_badges()
    bio = user_profile.get_bio()

    ##calculate wanted metrics 
    user_scores = ConnectionsScore.objects.filter(player_name=username)
    successful_puzzles = sum([obj.is_successful_puzzle() for obj in user_scores]) ##sums the results of the successful puzzle function
    total_puzzles = len(user_scores)

    avg_score_result = user_scores.aggregate(Avg('score_value'))
    avg_score_value = avg_score_result.get('score_value__avg') # Fetch the value, which might be None
    avg_score = round(avg_score_value if avg_score_value is not None else 0) # If avg_score_value is None, use default value 0; otherwise, use the fetched value
    
    #avg_score = round(avg_score_result.get('score_value__avg', 0))  # This will be None if there are no scores
    if len(user_scores) > 0:
        last_score_object = user_scores.order_by('puzzle_number', 'score_value').reverse()[0]
    else:
        last_score_object = None

    # Group scores by tens
    score_groups_nums = [(score.score_value // 10) * 10 for score in user_scores]  
    # Count occurrences in each group
    score_counts = Counter(score_groups_nums)  
    #finding the correct group to join 
    placeholder_groups = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    # for all the placeholder groups, if there is a number other than 0, return it 
    score_counts = [score_counts.get(group, 0) for group in placeholder_groups]
    #for the x axis 
    score_groups = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]

    # Convert Python lists to JSON for the graph to render
    score_groups_json = json.dumps(score_groups)
    score_counts_json = json.dumps(score_counts)




    return render(request, 'users/info.html', 
            {'profile': user_profile, 
            'user': user, 
            'bio': bio,

            #calculated metrics
            'avg_score':avg_score,
            'total_puzzles':total_puzzles,
            'successful_puzzles':successful_puzzles,
            'last_score_object':last_score_object,

            #for graph 
            'score_groups':score_groups_json,
            'score_counts':score_counts_json,
            
            'friends_profiles_following': friends_profiles_following,
            'friends_profiles_followers': friends_profiles_followers,
            'badges':badges})


class UserProfileAPIView(APIView):
    ##using the same view, but returning the api response instead of the html page
    def get(self, request, username):
        #Need immediate handler for no users, redirect to registration?
        if username == '':
            return redirect(reverse('users:register_view'))

        #obtain the instance of the profile and user based on the username on the page 
        user_profile = get_object_or_404(Profile, user__username=username)
        user = get_object_or_404(User, username=username)

        # Get the list of friends' profiles from the profile object method called get_friends_profiles_following/followers
        #also get badges and bio 
        friends_profiles_following = user_profile.get_friends_profiles_following()
        friends_profiles_followers = user_profile.get_friends_profiles_followers()
        badges = user_profile.get_badges()
        bio = user_profile.get_bio()

        ##calculate wanted metrics 
        user_scores = ConnectionsScore.objects.filter(player_name=username)
        successful_puzzles = sum([obj.is_successful_puzzle() for obj in user_scores]) ##sums the results of the successful puzzle function
        total_puzzles = len(user_scores)
        avg_score_result = user_scores.aggregate(Avg('score_value'))
        avg_score = round(avg_score_result.get('score_value__avg'))  # This will be None if there are no scores
        if len(user_scores) > 0:
            last_score_object = user_scores.order_by('puzzle_number', 'score_value').reverse()[0]
        else:
            last_score_object = None

        last_score_serialized = model_to_dict(last_score_object) #convert object to json serilazable 

        # Group scores by tens
        score_groups_nums = [(score.score_value // 10) * 10 for score in user_scores]  
        # Count occurrences in each group
        score_counts = Counter(score_groups_nums)  
        #finding the correct group to join 
        placeholder_groups = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        # for all the placeholder groups, if there is a number other than 0, return it 
        score_counts = [score_counts.get(group, 0) for group in placeholder_groups]
        #for the x axis 
        score_groups = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]

        # Convert Python lists to JSON for the graph to render
        score_groups_json = json.dumps(score_groups)
        score_counts_json = json.dumps(score_counts)

        print(last_score_object)
        

        return Response({#'profile': user_profile, 
                #'user': user, 
                'bio': bio,
                'avg_score':avg_score,
                'total_puzzles':total_puzzles,
                'successful_puzzles':successful_puzzles,
                'last_score_object':last_score_serialized,
                #'score_groups':model_to_dict(score_groups_json),
                #'score_counts':model_to_dict(score_counts_json),
                #'friends_profiles_following': model_to_dict(friends_profiles_following),
                #'friends_profiles_followers': model_to_dict(friends_profiles_followers),
                'badges':badges})

#serializer to convert complex data into json format 
def model_to_dict(instance):
    # Serialize the instance to JSON string and then convert to a dict
    return json.loads(serialize('json', [instance]))[0]['fields']

##this view listens for POST requests on the edit bio pages and will save the changes once the submit button is pressed 
def edit_bio_view(request, username):

    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user__username=username)
    # Get the list of friends' profiles from the profile object method called get_friends_profiles_following/followers
    #also get badges and bio 
    friends_profiles_following = user_profile.get_friends_profiles_following() #these are important so that the follower count remains consitent 
    friends_profiles_followers = user_profile.get_friends_profiles_followers()
    badges = user_profile.get_badges()
    bio = user_profile.get_bio() ##this is important so that the default is the current bio

    #if a user tries to edit a bio that is not theirs, they will be redirected back to their profile and prompt a threatening message 
    if request.user.username != username:
        messages.error(request, 'You think you are clever. You will be banned.')
        return redirect(reverse('users:user_profile', kwargs = {'username':request.user.username}))

    #handling of the form submission in which the new bio is saved 
    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        profile = request.user.profile
        profile.bio = bio
        profile.save()
        messages.success(request, 'Your bio has been updated.')
        return redirect(reverse('users:user_profile', kwargs={'username':username}))  # Adjust the redirect as needed

    #render the edit bio page with all information so that the navigation bar still looks clean 
    return render(request, 'users/edit_bio.html', 
        {'profile': user_profile, 
            'user': user, 
            'bio': bio,
            'friends_profiles_following': friends_profiles_following,
            'friends_profiles_followers': friends_profiles_followers,
            'badges':badges}
        )



def add_friend_view(request, user_id):
    # Default fallback URL if HTTP_REFERER is not available
    fallback_url = reverse('users:list_users')
    
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

            else:
                messages.error(request, "You cannot add yourself as a friend, silly goose.")
        else:
            messages.error(request, "You must be logged in to add friends.")
    else:
        messages.error(request, "Invalid request.")

    # Use the HTTP_REFERER header to redirect back to the previous page, if available
    return redirect(request.META.get('HTTP_REFERER', fallback_url))


def list_users_view(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/list_users.html', {'users': users})


def delete_relationship_view(request, friend_id):
    if request.method == "POST":
        # Assume the user initiating the request is the 'from_user'
        relationship = get_object_or_404(Friendship, from_user=request.user, to_user_id=friend_id)
        relationship.delete()
        messages.success(request, "Friendship removed successfully.")
    return redirect(reverse('users:following_list', kwargs={'username': request.user.username})) 


##render the following list html page which is an extension of the profile page 
def following_list_view(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    # Use existing method to get profiles of following users
    friends_profiles_following = user_profile.get_friends_profiles_following()
    friends_profiles_followers = user_profile.get_friends_profiles_followers()

    return render(request, 'users/following_list.html',{
            'profile': user_profile, 
            'user': user, 
            'friends_profiles_following': friends_profiles_following,
            'friends_profiles_followers': friends_profiles_followers})

##render the followers list html page which is an extension of the profile page 
def followers_list_view(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    # Use existing method to get profiles of follower users
    friends_profiles_followers = user_profile.get_friends_profiles_followers()
    friends_profiles_following = user_profile.get_friends_profiles_following()

    return render(request, 'users/followers_list.html', {
            'profile': user_profile, 
            'user': user, 
            'friends_profiles_following': friends_profiles_following,
            'friends_profiles_followers': friends_profiles_followers})


def badge_list_view(request, username):
    # Assuming you have a User model and a Profile model associated with it
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    
    # Emojis representing badges (you can replace these with your actual badge data)
    badges = user_profile.get_badges() #['🎖️', '🏅', '🎉', 'More badges coming soon...']
    # Use existing method to get profiles of follower users
    friends_profiles_followers = user_profile.get_friends_profiles_followers()
    friends_profiles_following = user_profile.get_friends_profiles_following()

    return render(request, 'users/badges.html', {
            'profile': user_profile, 
            'user': user, 
            'friends_profiles_following': friends_profiles_following,
            'friends_profiles_followers': friends_profiles_followers,
            'badges': badges})