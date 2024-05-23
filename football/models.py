from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
class CustomUser(AbstractUser):
    pass


class Positions(models.Model):
    position = models.CharField(max_length=50)

    def __str__(self):
        return self.position

class Team(models.Model):
    name = models.CharField(max_length=50)
    league = models.CharField(max_length=50)
    stadium = models.CharField(max_length=50)
    manager = models.CharField(max_length=50)
    players = models.ManyToManyField('Player', related_name="team_players")

    def __str__(self):
        return self.name
class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.ManyToManyField(Positions)
    age = models.IntegerField()
    free_agent = models.BooleanField(default=False)
    rating = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    worth = models.IntegerField()

    def __str__(self):
        return self.first_name


class League(models.Model):
    name = models.CharField(max_length=50)
    league_code= models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team, related_name="manager_league_teams")
    alive =models.BooleanField(default=True)

    def __str__(self):
        return self.name

class LeagueSeason(models.Model):
    league=models.ForeignKey(League, on_delete=models.SET_NULL, blank=True, null=True)
    season =models.CharField(max_length=50)

class LeagueTable(models.Model):
    league = models.ForeignKey(League, on_delete=models.SET_NULL, blank=True, null=True)
    season = models.ForeignKey(LeagueSeason, on_delete=models.SET_NULL, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    points = models.IntegerField()
    previous_position = models.IntegerField()
    won = models.IntegerField()
    lost = models.IntegerField()
    draw = models.IntegerField()
    played = models.IntegerField()
    goals_for = models.IntegerField()
    goals_against = models.IntegerField()

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='home_team', blank=True, null=True)
    away_team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='away_team', blank=True, null=True)
    home_team_goals = models.IntegerField()
    away_team_goals = models.IntegerField()
    date = models.DateField()
    league = models.ForeignKey(League, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.home_team + ' vs ' + self.away_team


class Transfers(models.Model):
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    league =models.ForeignKey(League, on_delete=models.SET_NULL, blank=True, null=True)
    is_trade=models.BooleanField(default=False)
    players_involved=models.ManyToManyField(Player, related_name='players_involved', blank=True)
    fee = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.player + ' to ' + self.team + ' for ' + self.fee
    def transfer_fee(self):
        total = 0
        if self.is_trade:
            for players in self.players_involved.all():
                offer += players.worth
                total = offer + self.fee
                if total < self.player.worth:
                    ValueError('Offer is less than player worth')
                else:
                    return total
        return self.fee
