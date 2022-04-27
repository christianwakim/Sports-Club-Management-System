from datetime import date
from email import message
from pickle import NONE
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from first_application.models import Annoucement, Field_Reservation, Reserved, User, Admin, Coach, Team, Player, Game
from first_application.forms import LoginForm, SignupForm, AdminLoginForm, TournamentForm, TournamenttForm, TrainersForm, TeamsForm, AcademyForm, joinTeamForm, ProfileUpdateForm, ProfileDeleteForm, rentForm, rentdayForm, CoachForm, TeamForm, CoachUpdateForm, AnnForm
from django.contrib import messages
from django.shortcuts import redirect, render
from datetime import datetime
from django.db.models import Value as V
from django.db.models.functions import Concat
from .decorators import user_login_required

# Create your views here.
def convTime(m2):
    if m2 == 'midnight':
        m2 = "00:00:00"
    elif m2 == 'noon':
        m2 = "12:00:00"
    else:
        m2 = m2.replace(".","")
        in_time = datetime.strptime(m2, "%I %p")
        out_time = datetime.strftime(in_time, "%H:%M:%S")
        m2 = out_time
    return m2

def getNextHour(time):
    hour = time.split(":")
    m = int(hour[0])+1
    if len(str(m))<2: #for hour less than 2 digits case done
        return("0"+str(m)+":"+hour[1]+":"+hour[2])
    elif str(m)=="24": #for 23:00 case done
        x = hour[0]='00'
        return(str(x)+":"+hour[1]+":"+hour[2])
    return(str(m)+":"+hour[1]+":"+hour[2])

def getweekday(weekday):
    res="Monday"
    if (weekday== "0"):
        res= "Monday"
    elif (weekday=="1"):
        res= "Tuesday"
    elif (weekday=="2"):
        res= "Wednesday"
    elif (weekday=="3"):
        res= "Thursday"
    elif (weekday=="4"):
        res= "Friday"
    elif (weekday=="5"):
        res= "Saturday"
    elif (weekday=="6"):
        res= "Sunday"
    return res

def index(request):
    user= get_user(request)
    games= Game.objects.all()
    news= Annoucement.objects.all()
    if (user==None):
        return render(request, 'index.html', {'games': games, 'news':news, 'user':user})
    else:
        return render(request, 'index.html', {'user':user, 'games':games, 'news':news, 'user': user})


def get_user(request):
    try:
        user= User.objects.get(user_id=request.session['user_id'])
        return user
    except Exception as e:
        #raise e
        return None

def get_coach(request):
    try:
        coach= Coach.objects.get(coach_id=request.session['coach_id'])
        return coach
    except Exception as e:
        #raise e
        return None

def get_tour(request):
    try:
        tour= Game.objects.get(game_id=request.session['game_id'])
        return tour
    except Exception as e:
        #raise e
        return None    

#This sections is reserved for functionalities related to the end-user, in terms of managing his account, updating it, deleting it, joining a team
#searching for coaches, reserving the club's field, ....
def login(request):
    form = LoginForm()
    adminform = AdminLoginForm()

    #someone hits submit
    if ('login' in request.POST and request.method == 'POST'):
        email= request.POST['email']
        password= request.POST['password']
        form= LoginForm(request.POST)
        news = Annoucement.objects.all()
        
        if (form.is_valid()):
            check = (User.objects.filter(email=email, password=password)).exists()
            check_email = (User.objects.filter(email=email)).exists()
            if (check_email== False):
                messages.success(request, 'User not registered. Please sign up')
            elif (check):
                user = User.objects.get(email=email, password=password)
                # messages.success(request, 'Login sucessful!') 
                request.session['user_id'] = user.user_id     
                return render(request, 'index.html', {'form':form, 'user':user, 'news': news})
            else:
                messages.success(request, 'Credentials incorrect!')

    if ('adminlogin' in request.POST):
        email= request.POST['email']
        password= request.POST['password']
        adminform= AdminLoginForm(request.POST)
        
        if (adminform.is_valid()):           
            check= (Admin.objects.filter(email=email, password=password)).exists()
            if (check):
                admin = Admin.objects.get(email=email, password=password)
                # messages.success(request, 'Login sucessful!') 
                request.session['admin_id'] = admin.admin_id   
                #return render(request, 'adminpagesearch.html')  
                return adminpage(request)
            else:
                messages.success(request, 'Credentials incorrect!')   

    return render(request, 'login.html', {'form': form, "adminform":adminform})



def signup(request):

    form= SignupForm()
    if (request.method=='POST'):
        first_name= request.POST['first_name']
        last_name=request.POST['last_name']
        email= request.POST['email']
        password= request.POST['password']
        date_of_birth= request.POST['date_of_birth']
        form= SignupForm(request.POST)

        if (form.is_valid()):
            check= (User.objects.filter(email=email)).exists()
            if (check== False):
                id_temp= User.objects.values('user_id').order_by('-user_id').first()['user_id']+1
                user= User.objects.create(user_id=id_temp,first_name= first_name, last_name= last_name, email=email, password= password, date_of_birth= date_of_birth)
                messages.success(request, 'Account succesfully created. Please sign in with your credentials!')
                return render(request, 'login.html',{'form': form,'user':user})
            else:
                messages.success(request, 'User already registered!')
                return render(request, 'signup.html')
        else:
            messages.success(request, 'Some error')
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')



def trainers(request):
    user = get_user(request)
    form = TeamsForm
    filtered_trainers = Coach.objects.all()
    if (request.method == "POST" and 'searchbutton' in request.POST):
        search = request.POST["search"]
        filtered_trainers = Coach.objects.annotate(full_name = Concat("first_name", V(" "),"last_name")).filter(full_name__icontains = str(search))
        if len(filtered_trainers) == 0:
            messages.success(request, 'Trainer does not exist!')
            return render(request, "trainers_test.html")
    return render(request, 'trainers_test.html', {'form': form, "filtered_trainers": filtered_trainers, "user": user})


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id'] # delete user session

    return redirect('index')


#facilities page
def services(request):
    user= get_user(request)
    return render(request, 'services.html', {'user': user})

#Reserve in sports academy under facilities page
@user_login_required
def academy(request):
    user = get_user(request)
    form = AcademyForm()
    return render(request, 'sportsacademy.html', {'user':user})


def DateValid(date_string):
    format = "%Y-%m-d"
    try:
        datetime.datetime.strptime(date_string, format)
        return True
    except:
        return False

@user_login_required
def edit(request):
    user = get_user(request)
    form= ProfileUpdateForm(instance=user)
    Reserv= Field_Reservation.objects.filter(user_ID= user)
    try:
        player =Player.objects.filter(user_ID= user.user_id)[:1].get()
    except Player.DoesNotExist:
        player= None
    if (player!=None):
        team= player.team_ID
    else:
        team= None
    if (request.method=='POST' and 'updatebutton' in request.POST):
        form= ProfileUpdateForm(request.POST, instance= user)
        if form.is_valid():
            date_of_birth= request.POST["date_of_birth"]
            year= date_of_birth.split("-")[0]
            if (int(year)>=2022 or int(year)<=1930):
                messages.success(request, "Date of Birth out of range. Select a suitable one!")
                return render(request, 'edit.html', {'form':form , 'user':user, 'Reserv':Reserv})

            form = form.cleaned_data
            dob= form['date_of_birth']
            if (DateValid(dob)==False):
                messages.success(request, "Invalid Date of Birth address. Try updating with a valid date of birth!")
                return render(request, 'edit.html', {'form':form , 'user':user})

            form.save()
            return render(request, 'index.html', {'form':form, 'user':user })
    else:
        return render(request, 'edit.html', {'form':form , 'user':user, 'Reserv':Reserv, 'team': team})

@user_login_required
def deleteUser(request):
    user = get_user(request)
    # user = get_object_or_404(User, id=id)
    # user = User.objects.get(id = id)
    # form= ProfileDeleteForm(instance=user)

    if (request.method=='POST' and 'deletebutton' in request.POST):
        user.delete()
        # return render(request, 'index.html')

    return render(request, 'index.html')


def availableteamscoaches(request):
    user = get_user(request)
    form = joinTeamForm
    filtered_teams = Team.objects.all()
    teams_list = [f.team_id for f in filtered_teams]

    if (request.method == "POST"):
        sport_select = request.POST["select"]
        cat= request.POST["select-1"]
        if (cat=="lt10"):
            cat= 1
        elif (cat=="10-13"):
            cat=2
        elif (cat=="14-17"):
            cat=3
        else:
            cat=4
        filtered_teams = Team.objects.filter(sports_type= sport_select, age_cat= cat)
        teams_list = [f.team_id for f in filtered_teams]
        request.session['filtered_teams'] = teams_list
        if len(filtered_teams) == 0:
            messages.success(request, 'No teams are found.')
            return render(request, "sportsacademy.html", {'form':form, 'user':user})
        return render(request, 'availableteamscoaches.html', {'form': form, "filtered_teams": filtered_teams, "user": user})
    else:
        request.session['filtered_teams'] = teams_list
        return render(request, "availableteamscoaches.html", {'user': user})

def FindKey(dict, target):
    for k,v in dict.items():
        if (v==target):
            return k

def age_compliant(dob, age_cat):
    import datetime
    td= datetime.datetime.now().date()
    bd= dob.date()
    age=int((td-bd).days /365.25)
    if (age_cat==1):
        return age <= 10
    elif (age_cat==2):
        return (age <= 13 and age >= 11)
    elif (age_cat==3):
        return (age <= 17 and age >= 14)
    elif (age_cat==4):
        return age >= 18


def jointeam(request):
    user = get_user(request)
    form = joinTeamForm()
    if (request.method=="POST"):
        #get the id of the team
        id_team = int(FindKey(request.POST, "Join Team"))
        team= Team.objects.filter(team_id= id_team)
        teamm= team[0]
        #check for capacity of team
        if (team.exists() and teamm.number_of_players+1> teamm.max_number_of_players):
            messages.success(request, 'Cannot join team because it is full. Try to go back and join another team.')
            return render(request, "testtest.html", {'team':team, 'user':user})
        
        #check for age requirements
        user_dob= user.date_of_birth
        age_comp= age_compliant(user_dob, teamm.age_cat)
        if (age_comp== False):
            messages.success(request, 'User age invalid with team age range. Join a team of user age range')
            return render(request, "testtest.html", {'team':team,  'user':user})

    if (Player.objects.filter(user_ID=user.user_id).exists()== False):
        #increment team capacity and add user in player database with reference to the team
        old= teamm.number_of_players
        Team.objects.filter(team_id= id_team).update(number_of_players= old+1)
        id_temp= Player.objects.values('player_id').order_by('-player_id').first()['player_id']+1
        player= Player.objects.create(player_id=id_temp, user_ID= user, team_ID= teamm)
        messages.success(request, 'User added to the team. He is now a player!')
        return render(request, "testtest.html", {'user': user, 'form': form, 'team':team, 'id_team':id_team, 'player':player})
    else:
        messages.success(request, 'User already in team!')
        return render(request, "testtest.html", {'user': user, 'form': form, 'team':team, 'id_team':id_team})


#Reserve fields under Reserve in facilities
@user_login_required
def rent(request):
    form= rentForm()
    user = get_user(request)
    if (request.method=="POST" and "reservee" in request.POST):
        #form= rentForm(request.POST)
        day= request.POST["day"]
        filtered_rentals = Reserved.objects.filter(day= day)
        exist= filtered_rentals.exists()
        if (exist== False):
            messages.success(request, "Cannot reserve field on the selected day. Can only reserve the field during the weekend")
        return render(request, 'rent_specialmonths.html', {'form': form, 'filtered_rentals': filtered_rentals, 'user':user})
    elif (request.method=="POST"):
        day= request.POST["day"]
        form= rentdayForm(request)
        St = FindKey(request.POST, "Reserve")
        St2= FindKey(request.POST, "Sport")
        St= convTime(St)
        #St2= request.GET[St2]
        Reserved.objects.filter(Starting_hour= St, day= day).update(Reserved= True) 
        id_temp= Field_Reservation.objects.values('reservation_id').order_by('-reservation_id').first()['reservation_id']+1
        end= getNextHour(St)
        Field_Reservation.objects.create(reservation_id=id_temp, user_ID= user, Date= day, Starting_hour= St, Ending_hour=end, with_equip= True, field_type= "Football", court_number=1)
        messages.success(request, "Field Succesfully booked!")
        return render(request, 'testtest.html', {'form': form, 'user':user, "St":St})
    return render(request, "rent_specialmonths.html")

#This sections is reserved for functionalities related to the System Admin: add a team, add a coach, add a tournament, add an annoucement to be displayed in the main page of the website.
#search and update, update score

def adminpage(request):
    return render(request, 'adminpage.html')



def createcoach(request):
    user = get_user(request)
    form= CoachForm()
    if (request.method=='POST' and 'addcoach' in request.POST):
        form= CoachForm(request.POST,request.FILES)
        if form.is_valid():
            id_temp= Coach.objects.values('coach_id').order_by('-coach_id').first()['coach_id']+1
            coachform = form.cleaned_data
            first = coachform['first_name']
            last = coachform['last_name']
            bio= coachform['biography']
            picture= coachform['picture']
            email= request.POST['email']
            if (Coach.objects.filter(email=email).exists()):
                messages.success(request,'coach already added!')
            else:
                messages.success(request,'Coach successfully added!')
                Coach.objects.create(coach_id= id_temp, first_name= first, last_name= last, phone_number=" ",email= email, biography= bio, picture=picture )
            return render(request, 'testtest.html', {'form':form, 'user':user })
    else:
        return render(request, 'createcoach.html', {'form':form , 'user':user})

def createteam(request):
    user = get_user(request)
    form= TeamForm()
    if (request.method=='POST'):
        form= TeamForm(request.POST)
        if form.is_valid():
            id_temp= Team.objects.values('team_id').order_by('-team_id').first()['team_id']+1
            teamform = form.cleaned_data
            teamname = teamform['team_name']
            des = teamform['team_description']
            coach= teamform['coach']
            tday= teamform['training_day']
            sh= teamform['Starting_hour']
            eh= teamform['Ending_hour']
            stype = request.POST.get('sport_type', False)
            age= request.POST.get('Agecategory', False)
            if (age=="less than 10"):
                cat=1
            elif (age=="11-13"):
                cat=2
            elif (age=="14-17"):
                cat=3
            else:
                cat=4
            if (Team.objects.filter(team_name= teamname).exists()):
                messages.success(request,'There exists a similar team of the same name. Please change its name')
            elif (Team.objects.filter(training_day= tday, Starting_hour= sh, Ending_hour= eh).exists()):
                messages.success(request,'There exists another team that practices on'+str(tday)+"from "+str(sh)+" to "+str(eh)+". Please pick another day and time")
            else:
                messages.success(request,'Team successfully added!')
                Team.objects.create(team_id= id_temp, team_name= teamname, team_description= des, number_of_players= 0, max_number_of_players= 20, sports_type= stype, age_cat= cat, coach= coach, training_day= tday, Starting_hour= sh, Ending_hour= eh)
            return render(request, 'testtest.html', {'form':form, 'user':user })
    else:
        return render(request, 'createteam.html', {'form':form , 'user':user})

def creategame(request):
    user = get_user(request)
    form= TournamenttForm()
    Teams= Team.objects.exclude(team_id=0)
    tournaments= Game.objects.exclude(game_id=0)
    if (request.method=='POST'):
        form= TournamenttForm(request.POST)
        if form.is_valid():
            id_temp= Game.objects.values('game_id').order_by('-game_id').first()['game_id']+1
            tform = form.cleaned_data
            sh = tform['Starting_hour']
            eh= tform['Ending_hour']
            team1_n= request.POST['select_team1']
            team2_n= request.POST['select_team2']
            Gameday= request.POST['Gameday']
            score= request.POST['score']
            #Check if two teams are of same type and same age
            team1= Team.objects.filter(team_name= team1_n)[:1].get()
            team2= Team.objects.filter(team_name= team2_n)[:1].get()
            int_weekday= str(datetime.strptime(Gameday, '%Y-%m-%d').weekday())
            str_weekday= getweekday(int_weekday)
            if (team1==team2):
                messages.success(request, "Cannot select the same team for team 1 and team2")
                return render(request, 'creategame.html', {'form':form, 'user':user, 'Teams': Teams })
            elif (team1.sports_type!=team2.sports_type):
                messages.success(request, "Selected teams must be teams of the same sports type")
                return render(request, 'creategame.html', {'form':form, 'user':user, 'Teams': Teams })
            elif (team1.age_cat!= team2.age_cat):
                messages.success(request, "Selected teams must be of the same age category")
                return render(request, 'creategame.html', {'form':form, 'user':user, 'Teams': Teams })
            elif (Game.objects.filter(Date= Gameday, Starting_hour=sh).exists()):
                messages.success(request, "There is another tournament being held during this time. Please change the timing")
                return render(request, 'creategame.html', {'form':form, 'user':user, 'Teams': Teams })
            elif (Team.objects.filter(training_day= str_weekday,Starting_hour= sh, Ending_hour= eh).exists()):
                messages.success(request, "There is a team practicing during this time. Please change the timing")
                return render(request, 'creategame.html', {'form':form, 'user':user, 'Teams': Teams })               
            Game.objects.create(game_id= id_temp, team_1_name= team1_n, team_2_name= team2_n, score= score, Date= Gameday, Starting_hour= sh, Ending_hour= eh )
            messages.success(request, "Tournament succesfully added!"+ str_weekday)
            return render(request, 'creategame.html', {'form':form, 'user':user, 'Teams': Teams })
    else:
        return render(request, 'creategame.html', {'form':form , 'user':user, 'Teams':Teams, 'tournaments': tournaments})


def delAnn(request):
    annouc= Annoucement.objects.all()
    if (request.method=="POST"):
        messages.success(request, "Old  and current annoucements succesfully deleted!")
        annouc.delete()
        
    return render(request, "delAnn.html")

def createAnn(request):
    user = get_user(request)
    form= AnnForm()
    if (request.method=='POST'):
        form= AnnForm(request.POST)
        if form.is_valid():
            tform = form.cleaned_data
            news = tform['news']
            Annoucement.objects.create(news=news)
            messages.success(request, "Annoucement succesfully added. Check the main page to see it!")
            return render(request, 'createAnn.html', {'form':form , 'user':user})
    return render(request, 'createAnn.html', {'form':form, 'user':user})



def adminsearch(request):
    coaches= Coach.objects.all()
    tournaments= Game.objects.all()
    teams= Team.objects.all()
    users= User.objects.all()
    return render(request, 'adminpagesearch.html', {'coaches':coaches, 'tournaments':tournaments, 'teams':teams, 'users':users, })

    
#     return render(request, "searchdisplay.html")

def searchforcoach(request):
    form = CoachUpdateForm()
    # form = TeamsForm
    filtered_trainers = Coach.objects.all()
    if (request.method == "POST" and 'searchbutton' in request.POST):
        search = request.POST["search"]
        filtered_trainers = Coach.objects.annotate(full_name = Concat("first_name", V(" "),"last_name")).filter(full_name__icontains = str(search))
        if len(filtered_trainers) == 0:
            messages.success(request, 'Trainer does not exist!')
            return render(request, "searchforcoach.html")
    Delete_coach = FindKey(request.POST, "Delete")
    Update_coach = FindKey(request.POST, "Update")
    if (request.method == "POST" and Delete_coach in request.POST):
        coach_to_be_deleted = Coach.objects.get(coach_id = Delete_coach)
        coach_to_be_deleted.delete()
    if (request.method == "POST" and Update_coach in request.POST):
        coach_to_be_up = Coach.objects.get(last_name = Update_coach)
        request.session['coach_id'] = coach_to_be_up.coach_id
        form= CoachUpdateForm(instance=coach_to_be_up)
        return render(request, "adupdatecoach.html", {"filtered_trainers": filtered_trainers, 'form':form})
       
    return render(request, "searchforcoach.html", {"filtered_trainers": filtered_trainers})

def adupdatecoach(request):
    form= CoachUpdateForm()
    coachh= get_coach(request)
    if (request.method=='POST'):
        form= CoachUpdateForm(request.POST, instance= coachh)
        if form.is_valid():
            form = form.cleaned_data
            coach= Coach.objects.filter(coach_id= coachh.coach_id).update(first_name= form['first_name'],last_name= form['last_name'], biography= form['biography'],email= form['email'])
            messages.success(request, "Success in updating tournament!")
            return render(request, "adupdatecoach.html", {'fform':form})
        return render(request, "adupdatecoach.html", {'fform':form})
    return render(request, "adupdatecoach.html")

def searchforteam(request):
    return render(request, "searchforteam.html")

def valid_score(element):
    L=["0","1","2","3","4"]
    return (element in L )

def updatetournament(request):
    form= TournamentForm()
    tour= get_tour(request)
    coachh= get_coach(request)
    if (request.method=='POST'):
        form= TournamentForm(request.POST, instance= tour)
        if form.is_valid():
            form = form.cleaned_data
            score= form['score']
            score_l= score.split("-")
            if (len(score_l)!=2):
                messages.success(request, "Invalid score. Cannot update score")
                return render(request, "adupdatecoach.html", {'fform':form})
            elif (valid_score(score_l[0])==False or valid_score(score_l[1])==False):
                messages.success(request, "Invalid score. Cannot update score")
                return render(request, "adupdatecoach.html", {'fform':form})
            else:
                tour= Game.objects.filter(game_id= tour.game_id).update(team_1_name= form['team_1_name'],team_2_name= form['team_2_name'], score= form['score'], Date= form['Date'], Starting_hour= form['Starting_hour'], Ending_hour= form['Ending_hour'])
                messages.success(request, "Success in updating score")
                return render(request, "adupdatecoach.html", {'fform':form})
        return render(request, "adupdatecoach.html", {'fform':form})
    return render(request, "adupdatecoach.html")

def searchfortournament(request):
    form = TournamentForm()
    if (request.method == "POST"):
        t1 = request.POST["Team 1 name"]
        t2 = request.POST["Team 2 name"]
        tour= Game.objects.filter(team_1_name= t1, team_2_name= t2)[:1].get()
        form= TournamentForm(instance= tour)
        request.session['game_id'] = tour.game_id
        return render(request, "updatetournament.html", {'form':form})
    return render(request, "seachfortournament.html", {"form": form})




