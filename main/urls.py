from django.urls import path, include
from . import views
from .views import index, addMemes
app_name = "main"

urlpatterns = [
    path('', index.as_view(), name="index"),
    path('trending/', views.trend, name="trending"),
    path('favourites/', views.favourites, name='favourites'),
    path('add/memes/', addMemes.as_view(), name="add-memes"),
    path('see/memes/<int:pk>/', views.seeMemes, name="see-memes"),
    path('like/memes/', views.like, name='like-memes'),
    path('delete/memes/<int:pk>/', views.deleteMemes, name="delete-memes"),
    path('bookmark/memes/<int:pk>/', views.bookmarkMemes, name="bookmark-memes"),
]
