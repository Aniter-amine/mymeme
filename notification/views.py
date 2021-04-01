from django.contrib.auth.decorators import login_required
from notification.models import Notification
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


@login_required(login_url='login')
def seeNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(
        receiver=user).order_by("-date")
    template = loader.get_template("notifications.html")
    context = {
        "notifications": notifications,
    }
    return HttpResponse(template.render(context, request))
