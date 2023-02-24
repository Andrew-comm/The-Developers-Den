from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.
from .models import Room,Topic
from .forms import RoomForm


def home_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)) 
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count}    
    return render(request, "home.html",context)


def room(request,pk):
    room = Room.objects.get(id=pk)   
    context={'room':room}
    return render(request,'room.html',context)


def makeRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()      
    
    context = {'form': form}   
    return render(request,'room_form.html',context)



def modifyRoom(request,pk):
    room = Room.objects.get(id=pk)  
    form = RoomForm(instance=room)
    context={'form':form}

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()

    return render(request,'room_form.html',context)

def eliminateRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, "delete.html", {'obj':room})


