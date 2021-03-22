from django.contrib import admin
from .models import Post,Comment,Like

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "desc",
        "upload_on",
    ]
    def name(self,obj):
        return obj.user.first_name+" "+obj.user.last_name

class LikeAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "time",
    ]

class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "comment",
        "time",
    ]

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Like,LikeAdmin)