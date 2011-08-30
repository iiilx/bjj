from django.contrib import admin
from bjj.app.models import *

class PostAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

