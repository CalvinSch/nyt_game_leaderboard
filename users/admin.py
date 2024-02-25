from django.contrib import admin

# Register your models here.
#from .models import Flight, Airport, Passenger

# #if i want more info on a flight, for example, add more fields 
# class FlightAdmin(admin.ModelAdmin):
#     #this will just show more fields in teh admin UI
#     list_display = ("id", "origin", "destination", "duration")


# class PassengerAdmin(admin.ModelAdmin):
#     #will show the flights a passenger is on in a better way 
#     filter_horizontal = ("flights",)

# admin.site.register(Airport)
# admin.site.register(Flight, FlightAdmin) #use the flightadmin settings when you view in teh interface 
# admin.site.register(Passenger, PassengerAdmin)
