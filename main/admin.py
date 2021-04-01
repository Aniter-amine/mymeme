from django.contrib import admin
from .models import Memes, Comment


class MemesAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['body', 'user__username', 'user__email']

    class Meta:
        model = Memes


admin.site.register(Memes, MemesAdmin)
admin.site.register(Comment)
