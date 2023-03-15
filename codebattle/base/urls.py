from django.urls import path
from . import views

urlpatterns = [
   path('login', views.login_page, name="login"),
   path('logout', views.logoutUser, name="logout"),
   path('register', views.registerUser, name="register"), 
 
   
   path('', views.home_page, name="home"),
   path('room/<int:pk>/', views.room, name="room"),
   path('create-room/', views.makeRoom, name="create-room"),
   path('update-room/<str:pk>/', views.modifyRoom, name="update-room"),
   path('delete-room/<str:pk>/', views.eliminateRoom, name="delete-room"),
   path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

  

]
