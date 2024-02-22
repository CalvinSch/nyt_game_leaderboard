from django.db import models

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class ConnectionsScore(models.Model):
    
    #Sample Connections text output:
    """
    Connections 
    Puzzle #255
    🟨🟩🟪🟨
    🟨🟨🟨🟨
    🟪🟩🟩🟦
    🟪🟩🟩🟩
    🟩🟩🟪🟩

    Connections 
    Puzzle #255
    🟪🟪🟪🟪
    🟩🟩🟩🟩
    🟨🟨🟨🟨
    🟦🟦🟦🟦
    """

    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    player_name = models.CharField(max_length = 100)
    puzzle_number = models.IntegerField(null = True, blank = True)
    score_details = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.player_name} - {self.puzzle_number} - Puzzle #{self.puzzle_number}"

