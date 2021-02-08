from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.loginPg, name='login'),
    path('home/', views.home, name='home'), # All movies (buy tickets) 
    path('tickets/', views.tickets, name='tickets'), # User can see his chosen tickets 
    path('logout/', views.logoutPg, name='logout'),
    path('staffonly/', views.StaffOnly, name='staffonly'), # Staff view
    path('add/', views.Add_a_movie, name='add'),
    path('BuyTicket/<int:mid>', views.BuyTicket, name='BuyTicket'),
    path('DeleteMovie/<int:mid>', views.DeleteMovie, name='DeleteMovie'),
    path('DeleteTicket/<int:tid>/<int:mid>', views.DeleteTicket, name='DeleteTicket'),
]
#<str:pk>/