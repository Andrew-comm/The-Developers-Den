from django.shortcuts import render

# Create your views here.

from .models import Room

# rooms = [
#     {'id':1, 'name' : 'python'},
#     { 'id':2, 'name' : 'Web design'},
#     ]



# Create your views here.
def home_page(request):
    rooms=Room.objects.all()
    context = {'rooms':rooms}
    
    return render(request, "home.html",context)


def room_page(request,pk):
    room = Room.objects.get(id=pk)   
    context={'room':room}
    return render(request,'room.html',context)
    



