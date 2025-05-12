from django.contrib import admin

from core.models import DogUserModel

@admin.register(DogUserModel)
class DogUserAdmin(admin.ModelAdmin):
    pass
