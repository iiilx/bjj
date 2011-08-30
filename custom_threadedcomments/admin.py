from django.contrib import admin
from bjj.custom_threadedcomments.models import CustomThreadedComment

class CustomThreadedCommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomThreadedComment, CustomThreadedCommentAdmin)
