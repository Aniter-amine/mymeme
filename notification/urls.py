from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.seeNotifications, name="see-notifications")
]
