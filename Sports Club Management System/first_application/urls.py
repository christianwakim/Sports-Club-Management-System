from django.conf.urls import url
from django.urls import path
from first_application import views


urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^login',views.login, name='login'),
    url(r'^signup',views.signup, name='signup'),
    url(r'^trainers_test', views.trainers, name='trainers_test'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^services', views.services, name = 'services'),
    url(r'^academy', views.academy, name = 'academy'),
    url(r'^availableteamscoaches', views.availableteamscoaches, name= 'availableteamscoaches'),
    url(r'^jointeam', views.jointeam, name= 'jointeam'),
    url(r'^edit', views.edit, name= 'edit'),
    url(r'^delete', views.deleteUser, name="delete"),
    url(r'^rent', views.rent, name='rent'),
    url(r'^adminpage', views.adminpage, name='adminpage'),
    url(r'^createcoach', views.createcoach, name="createcoach"),
    url(r'^creategame', views.creategame, name="creategame"),
    url(r'^createteam', views.createteam, name="createteam"),
    url(r'^createAnn', views.createAnn, name="createAnn"),
    url(r'^delAnn', views.delAnn, name="delAnn"),
    url(r'^adminsearch', views.adminsearch, name="adminsearch"),
    url(r'^searchforcoach', views.searchforcoach, name="searchforcoach"),
    url(r'^adupdatecoach', views.adupdatecoach, name="adupdatecoach"),
    url(r'^searchfortournament', views.searchfortournament, name="searchfortournament"),
    url(r'^updatetournament', views.updatetournament, name="updatetournament"),
    url(r'^searchforteam', views.searchforteam, name="searchforteam"),
    ]
