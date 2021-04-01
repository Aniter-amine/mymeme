from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Notification(models.Model):
    NOTIFICATION_TYPE = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    meme = models.ForeignKey(
        "main.Memes", on_delete=models.CASCADE, related_name="notification_post", blank=True, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_receiver")
    text = models.CharField(max_length=90, blank=True)
    message = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
