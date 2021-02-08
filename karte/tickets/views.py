from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user, get_user_model, authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import VisitorForm, MovieForm, UserForm
from .models import Movies, Ticket, User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
# Create your views here.

def register(request):
        if request.method == "POST":
            username = request.POST.get('username', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            password = request.POST.get('password1', '')
            useremail = request.POST.get('email', '')
            form = VisitorForm(request.POST)
            user = auth.authenticate(request, useremail=useremail, password=password)
            if user is None and form.is_valid():
                user = get_user_model().objects.create_user(username=username,first_name=first_name, last_name=last_name, password=password, email=useremail)
                user.save()
                response = HttpResponseRedirect('/login')
                return response
            else:
                messages.error(request, f'Something went wrong!')
                
        elif request.method == "GET":
            return render(request, 'register.html', {'form':VisitorForm})
        #response = HttpResponseRedirect('/register',{'msg':'An error occured'})
        #return response
        return render(request, 'register.html', {'form':VisitorForm})

def loginPg(request):
    form=AuthenticationForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            messages.success(request, f'An error occured!')
            return HttpResponseRedirect('/login')
    if request.method == "GET":        
        return render(request, 'login.html', {'form':form})
def logoutPg(request):
    logout(request)
    messages.success(request, f'You have been logged out successfully!')
    response = HttpResponseRedirect('/login')
    # Redirect to a success page.
    return response

@login_required(login_url='login')
def home(request):
    movies = Movies.objects.all()
    return render(request, template_name='home.html', context= {'movies':movies})

@login_required(login_url='login')
def tickets(request):
    tck=Ticket.objects.all()
    user=request.user
    tickets = Ticket.objects.filter(user=user.id)
    return render(request, 'tickets.html', context = {'tickets':tickets,'user':user})

def BuyTicket(request,mid):
    movie = Movies.objects.get(id=mid)
    if movie.TotalSeat > 0:
        addticket = Ticket(user = request.user, MovieName=movie, Seat =  movie.TotalSeat)
        movie.TotalSeat =movie.TotalSeat - 1
        movie.save()
        addticket.save()    
    return redirect('home')

def DeleteTicket(request, tid, mid):
    ticket = Ticket.objects.get(id_ticket=tid)
    movie = Movies.objects.get(id = mid)
    movie.TotalSeat = movie.TotalSeat + 1
    movie.save()
    ticket.delete()  
    return redirect('tickets')

def DeleteMovie(request,mid):
    movie = Movies.objects.get(id=mid)
    movie.delete()   
    return redirect('home')

#Buying the ticket
def Add_a_movie(request):
    user = request.user
    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    return render(request, 'add.html', context = {'form':form, 'user':user})


def StaffOnly(request):
    maxBroj = 0
    movies = Movies.objects.all()
    karta = Ticket.objects.all()
    usr = User.objects.all()
    total_tickets = karta.count()
#User with most tickets
    for item in karta:
        usrtck = karta.filter(user=item.user)
        for u in usrtck:
            total_tck = karta.filter(MovieName=item.MovieName).count()
            if total_tck > maxBroj:
                maxBroj = total_tck
                najvise = u.user
    return render(request, template_name='staffonly.html', context = {'movies':movies, 'usr':usr, 'total_tickets':total_tickets, 'najvise':najvise,'maxBroj':maxBroj,'karta':karta})


# Adding Users as Staff 
    if request.method =='POST':
        stat = request.POST.get('status')
        usrn = request.POST.get('Add')
        usr_obj = User.objects.get(username=usrn)
        
        if stat == 'True':
            usr_obj.is_staff = True
            usr_obj.save()
        return render(request, template_name='staffonly.html', context = {'movies':movies,'karta':karta, 'usr':usr, 'usrn':usrn, 'total_tickets':total_tickets})   
    return render(request, template_name='staffonly.html', context = {'movies':movies,'karta':karta, 'usr':usr, 'total_tickets':total_tickets, 'maxBroj':maxBroj})

 #       if form.is_valid():
  #          form.UserForm(instance=usr)
   #         form.save()  
   #        return HttpResponseRedirect('staffonly/')
   #     else:
    #        return render(request, 'addusr.html', context = {'form':form, 'a':a})
