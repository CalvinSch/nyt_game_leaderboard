from django.shortcuts import render, redirect, get_object_or_404
from .forms import ConnectionsScoreForm
from .models import ConnectionsScore
from users.models import Profile, User
from users.views import user_profile_view

# Create your views here.
def leaderboard_view(request):
    leaderboard_scores = ConnectionsScore.objects.order_by('puzzle_number', 'score_value').reverse()

    #following_ids =
    #following_scores = request.user.friend_user_ids

    context = {'leaderboard_scores': leaderboard_scores}
    return render(request, 'leaderboards/global_leaderboard.html', context)

def submit_score(request):
    if request.method == "POST":
        form =  ConnectionsScoreForm(request.POST, player_name = request.user.username)
        if form.is_valid():
            form.save()
            return redirect('leaderboards:leaderboard') #Redirect to leaderboard page, which has the '' url
    else:
        form = ConnectionsScoreForm()
    
    return render(request, 'leaderboards/submit_score.html', {'form': form})
    
    
# Create your views here.
def leaderboard_view_following(request, username):
    leaderboard_scores = ConnectionsScore.objects.order_by('puzzle_number', 'score_value').reverse()

    #if user is not authenticated, return to leaderboard view with a message saying you must be logged in 
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to see following leaderboard.")
        return redirect(reverse('leaderboards:leaderboard_view'))
    if username == 'PLACEHOLDER':
        messages.error(request, "You must be logged in to see following leaderboard.")
        return redirect(reverse('leaderboards:leaderboard_view'))

    #obtain the instance of the profile and user based on the username on the page 
    user_profile = get_object_or_404(Profile, user__username=username)
    user = get_object_or_404(User, username=username)

    # Get the list of friends' profiles from the profile object method called get_friends_profiles_following/followers 
    friends_profiles_following = user_profile.get_friends_profiles_following()
    friends_users_following = []
    for friend_profile in friends_profiles_following:
        friends_users_following.append(friend_profile.user.username)
    
    
    print(f'users_following: {friends_users_following}')

    needed_users = []
    for score in leaderboard_scores:
        needed_users.append(score.player_name)

    print(needed_users)


    context = {'leaderboard_scores': leaderboard_scores,
                'needed_users':needed_users,
                'user': user, 
                'friends_profiles_following': friends_users_following}
    return render(request, 'leaderboards/following_leaderboard.html', context)