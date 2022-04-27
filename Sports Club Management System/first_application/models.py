from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
#The database will consist of multiple tables: users, players, coaches, admin, teams, reservations, events, games

#Users table
class User(models.Model):
    user_id= models.IntegerField(primary_key=True)
    first_name= models.CharField(max_length=30)
    last_name= models.CharField(max_length=30)
    email= models.EmailField(max_length=30)
    password= models.CharField(max_length=30)
    date_of_birth= models.DateTimeField(default=timezone.now)
    #gender= models.CharField(max_length=6)
    
#Admin Table
class Admin(models.Model):
    admin_id= models.IntegerField(primary_key=True)
    email= models.EmailField(max_length=30)
    password= models.CharField(max_length=30)

#Coaches Table
class Coach(models.Model):
    coach_id= models.IntegerField(primary_key=True)
    biography = models.CharField(max_length=200, default="Bio")
    first_name= models.CharField(max_length=30)
    last_name= models.CharField(max_length=30)
    phone_number= models.CharField(max_length=30)
    email= models.CharField(max_length=30)
    picture = models.ImageField(null= True, blank= True)

#Team Table
class Team(models.Model):
    team_name= models.CharField(max_length=30)
    team_id= models.IntegerField(primary_key=True)
    team_description= models.TextField(default="some description")
    number_of_players= models.IntegerField()
    max_number_of_players= models.IntegerField(default=30)
    sports_type= models.CharField(max_length=30)
    age_cat= models.IntegerField(default=1)
    #age cat is 1 for age <10, 2 for 11-13, 3 for 14-17 and 4 for 18+
    coach= models.ForeignKey(Coach, on_delete= models.CASCADE)
    training_day= models.CharField( max_length= 10, default="Monday")
    Starting_hour= models.TimeField(default="00:00:00" )
    Ending_hour= models.TimeField(default= "00:00:00")

#Players Table
class Player(models.Model):
    player_id= models.IntegerField(primary_key=True)
    user_ID= models.ForeignKey(User,on_delete=models.CASCADE)
    team_ID= models.ForeignKey(Team,on_delete=models.CASCADE)


#Reservations Table
class Field_Reservation(models.Model):
    reservation_id= models.IntegerField(primary_key=True)
    user_ID= models.ForeignKey(User,on_delete=models.CASCADE)
    Date = models.DateTimeField(default=datetime.now)
    Starting_hour= models.CharField(max_length= 30)
    Ending_hour= models.CharField(max_length= 30)
    with_equip= models.BooleanField()
    field_type= models.CharField(max_length= 30)
    court_number= models.IntegerField()

#Events Table: any event different than team joining or game
class Event(models.Model):
    event_id= models.IntegerField(primary_key=True)
    user_ID= models.ForeignKey(User,on_delete=models.CASCADE)
    with_food= models.BooleanField()
    Date = models.DateTimeField(default=datetime.now)
    Starting_hour= models.CharField(max_length= 30)
    Ending_hour= models.CharField(max_length= 30)


#Games Table
class Game(models.Model):
    game_id= models.IntegerField(primary_key=True)
    team_1_name= models.CharField(max_length=30)
    team_2_name= models.CharField(max_length=30)
    score = models.CharField(max_length=6)
    Date= models.DateField(default=datetime.now)
    Starting_hour= models.TimeField(default="00:00:00" )
    Ending_hour= models.TimeField(default= "00:00:00")

#This table is for field reservations, an extension of the Field_Reservations table to allow a better calendar visulization in the website
class Reserved(models.Model):
    day=models.DateTimeField(default=datetime.now)
    Starting_hour= models.TimeField()
    Ending_hour= models.TimeField()
    Reserved= models.BooleanField()

class Annoucement(models.Model):
    news= models.TextField()
