from django.shortcuts import render, redirect
from .forms import ConnectionsScoreForm
from .models import ConnectionsScore

# Create your views here.
def leaderboard_view(request):
    leaderboard_scores = ConnectionsScore.objects.order_by('puzzle_number', 'score_value').reverse()

    context = {'leaderboard_scores': leaderboard_scores}
    return render(request, 'leaderboards/leaderboard.html', context)

def submit_score(request):
    if request.method == "POST":
        form =  ConnectionsScoreForm(request.POST, player_name = request.user.username)
        if form.is_valid():
            form.save()
            return redirect('leaderboards:leaderboard') #Redirect to leaderboard page, which has the '' url
    else:
        form = ConnectionsScoreForm()
    
    return render(request, 'leaderboards/submit_score.html', {'form': form})
    
