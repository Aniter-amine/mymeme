from django.contrib.auth.models import User
from django.db.models.signals import post_save
from notification.models import Notification
from django.urls import reverse
from django.db import models
import uuid
import os


# Path Of Video Model
def get_memes_picture_upload_path(instance, header_image):
    return os.path.join(
        f"pictures/memes/{ instance.user.id }/{ instance.id }.jpg")


# Path Of Video Model
def get_memes_video_upload_path(instance, header_image):
    return os.path.join(
        f"video/memes/{ instance.user.id }/{ instance.id }.mp4")


# Memes Favourites Model
class MemesFavourites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True)
    memes = models.ForeignKey(
        "Memes", on_delete=models.CASCADE, blank=True)
    date = models.DateTimeField(auto_now_add=True)


# Memes Model
class Memes(models.Model):
    def get_uuid_no_dash():
        sd = str(uuid.uuid4().int)[:16]
        return int(sd)

    id = models.AutoField(
        primary_key=True, default=get_uuid_no_dash, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True)
    favourites = models.ManyToManyField(
        User, related_name='favourite', default=None, blank=True, through=MemesFavourites)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    like_count = models.BigIntegerField(default=0)
    body = models.CharField(max_length=256)
    image = models.ImageField(
        blank=True, upload_to=get_memes_picture_upload_path)
    video = models.FileField(blank=True, upload_to=get_memes_video_upload_path)
    date = models.DateTimeField(auto_now_add=True)
    views = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.views} • {self.date} |  {self.body}'

    def get_absolute_url(self):
        return reverse("main:see-memes", kwargs={"pk": self.id})

    def get_like_url(self):
        return reverse("main:like-toggle-memes", kwargs={"pk": self.id})

    def get_like_api_url(self):
        return reverse("main:like-toggle-api-memes", kwargs={"pk": self.id})


# Comment Model
class Comment(models.Model):
    meme = models.ForeignKey(
        Memes, on_delete=models.CASCADE, related_name='comments', null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Comment by {self.user} | Text: {self.body}'

    def user_comment_meme(sender, instance, *args, **kwargs):
        comment = instance
        meme = comment.meme
        sender = comment.user
        receiver = meme.user
        text = comment.body
        notify = Notification(meme=meme, sender=sender,
                              receiver=receiver, notification_type=2, text=text, message="Commented To Your Meme")
        notify.save()


# Comment Signal
post_save.connect(Comment.user_comment_meme, sender=Comment)
