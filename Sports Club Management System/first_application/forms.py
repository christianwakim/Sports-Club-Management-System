
from django import forms
from first_application.models import Annoucement, Field_Reservation, Game, Reserved, User, Admin, Coach, Team

#form for login
class LoginForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ['email', 'password']


#form for Signup
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password', 'date_of_birth']


#form for Admin login
class AdminLoginForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['email', 'password']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model= User
        fields= ['first_name','last_name','email','password', 'date_of_birth']

class ProfileDeleteForm(forms.ModelForm):
    class Meta:
        model= User
        fields=['first_name','last_name','email','password', 'date_of_birth']

#form for Trainers
class TrainersForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['coach_id', 'biography', 'first_name', 'last_name', 'email', 'picture']

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['first_name', 'last_name', 'biography', 'picture']

#form for Team
class TeamsForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name','team_id','number_of_players','sports_type']

class TeamForm(forms.ModelForm):
    class Meta:
        model= Team
        fields = ['team_name','team_description','coach', 'training_day', 'Starting_hour', 'Ending_hour']


class AcademyForm(forms.ModelForm):
    class Meta:
        model= Team
        fields = ['team_name','team_id','number_of_players','sports_type']

class joinTeamForm(forms.ModelForm):
    class Meta:
        model= Team
        fields = ['team_name','team_id','number_of_players','sports_type']


class rentForm(forms.ModelForm):
    class Meta:
        model= Field_Reservation
        fields=['reservation_id','user_ID','Date' ,'Starting_hour','Ending_hour','with_equip','field_type','court_number']

class rentdayForm(forms.ModelForm):
    class Meta:
        model= Reserved
        fields= ['day', 'Starting_hour', 'Ending_hour', 'Reserved']

class TournamentForm(forms.ModelForm):
    class Meta:
        model= Game
        fields= ['team_1_name', 'team_2_name', 'score', 'Date', 'Starting_hour', 'Ending_hour']
        
class GameForm(forms.ModelForm):
    class Meta:
        model= Game
        fields= ['score'] 

class TournamenttForm(forms.ModelForm):
    class Meta:
        model=Game
        fields= [ 'Starting_hour', 'Ending_hour']

class CoachUpdateForm(forms.ModelForm):
    class Meta:
        model= Coach
        fields= ['first_name','last_name','biography', 'email']

class AnnForm(forms.ModelForm):
    class Meta:
        model= Annoucement
        fields= ['news']

