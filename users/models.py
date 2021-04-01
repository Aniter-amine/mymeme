from django.db.models.signals import post_save, post_delete
from notification.models import Notification
from django.contrib.auth.models import User
from main.models import Memes
from django.db import models


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='following')

    def user_follow(sender, instance, *args, **kwargs):
        sender = instance.follower
        receiver = instance.following
        notify = Notification.objects.filter(
            sender=sender, receiver=receiver, notification_type=3)
        notify.delete()
        notify = Notification(sender=sender,
                              receiver=receiver, notification_type=3, message="Start Following You")
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        sender = instance.follower
        receiver = instance.following

        notify = Notification.objects.filter(
            sender=sender, receiver=receiver, notification_type=3)
        notify.delete()
        notify = Notification(sender=sender,
                              receiver=receiver, notification_type=3, message="Stoped Following You")
        notify.save()


# Comment
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)
