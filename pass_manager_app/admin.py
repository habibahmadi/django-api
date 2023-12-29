from django.contrib import admin
from pass_manager_app import models 

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)