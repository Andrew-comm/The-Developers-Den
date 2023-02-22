from django.urls import path
from . import views

urlpatterns = [
   path('',views.home_page, name="home"),
   path('room_page/<str:pk>/',views.room_page, name="room"),
]