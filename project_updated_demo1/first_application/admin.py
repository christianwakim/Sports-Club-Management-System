from django.contrib import admin
from first_application.models import User, Admin, Team , Coach, Player, Field_Reservation, Event, Game, Reserved, Annoucement


# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Team)
admin.site.register(Coach)
admin.site.register(Player)
admin.site.register(Field_Reservation)
admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Reserved)
admin.site.register(Annoucement)