from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.userLogin, name="user-login"),
    path('logout/', views.userLogout, name="user-logout"),
    path('<username>/', views.userProfile, name="profile"),
    path('<username>/followers/', views.userProfileFollowers, name="followers"),
    path('<username>/following/', views.userProfilefollowing, name="following"),
    path('follow/<username>', views.follow, name='follow'),
]
