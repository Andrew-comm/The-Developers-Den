from django.urls import path
from . import views

urlpatterns = [
   path('login', views.login_page, name="login"),
   path('logout', views.logoutUser, name="logout"),
   path('register', views.registerUser, name="register"),
   path('about', views.aboutPage, name="about"),  
      
 
 
 
   
   path('', views.home_page, name="home"),
   path('room/<int:pk>/', views.room, name="room"),
   path('profile/<int:pk>/', views.userProfile, name="profile"),

   path('create-room/', views.makeRoom, name="create-room"),
   path('update-room/<str:pk>/', views.modifyRoom, name="update-room"),
   path('delete-room/<str:pk>/', views.eliminateRoom, name="delete-room"),
   path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
   path('update-profile/', views.updateProfile, name="update-profile"),
   path('dashboard/', views.dashboardPage, name="dashboard"),
   path('topics/', views.topicsPage, name="topics"),
   path('activity/', views.activityPage, name="activity"),
   path('contact/', views.contactPage, name="contact"),



  

]
