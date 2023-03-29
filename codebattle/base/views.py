from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Room,Topic,Message
from .forms import RoomForm


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username  = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if a user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User doesn't exist")
            return render(request, 'login_register.html')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is invalid')

    context = {'page':page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration")

    context = {'form':form}
    
    return render(request, "login_register.html",context)

def home_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # Get all rooms that match the search query
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    # Get all topics for filtering
    topics = Topic.objects.all()
    
    # Get the total count of rooms that match the search query
    room_count = rooms.count()
    
    # Get all messages of rooms that match the search query
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # Create a dictionary to hold the context data
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
        'q': q,
    }

    # Render the home.html template with the context data
    return render(request, 'home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')



        )
        room.participants.add(request.user)   
        return redirect('room', pk=room.id)
    
    context={'room':room,'room_messages':room_messages, 'participants':participants}
    return render(request,'room.html',context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request,'profile.html',context)

@login_required(login_url='login')
def makeRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name='topic_name')

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
       
        return redirect('home')      
    
    context = {'form': form, 'topics':topics}   
    return render(request,'room_form.html',context, )


@login_required(login_url='login')
def modifyRoom(request,pk):
    room = Room.objects.get(id=pk)  
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    context={'form':form, 'topics':topics, 'room':room}

    if request.user != room.host:
        return HttpResponse("You have no capability to edit this space!!")

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()

    return render(request,'room_form.html',context)

@login_required(login_url='login')
def eliminateRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You have no permission to delete this space!!")


    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, "delete.html", {'obj':room})


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You have no permission to delete this message!!")


    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, "delete.html", {'obj':message})

@login_required(login_url='login')
def aboutPage(request):
    context={}
    return render(request,'about.html', context)


@login_required(login_url='login')
def updateProfile(request):
    return render(request, 'update-profile.html')

def dashboardPage(request):
    return render(request, 'dashboard.html')

