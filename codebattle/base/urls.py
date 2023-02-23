from django.urls import path
from . import views

urlpatterns = [
   path('', views.home_page, name="home"),
   path('room/<int:pk>/', views.room, name="room"),
   path('create-room/', views.makeRoom, name="create-room"),
   path('update-room/<str:pk>/', views.modifyRoom, name="update-room"),
  

]
