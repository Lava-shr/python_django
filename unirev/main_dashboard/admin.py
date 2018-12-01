from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Users)
class ModelAdmin(admin.ModelAdmin): pass

@admin.register(Userimage)
class ModelAdmin(admin.ModelAdmin): pass

@admin.register(Universities)
class ModelAdmin(admin.ModelAdmin): pass

@admin.register(Uniimage)
class ModelAdmin(admin.ModelAdmin): pass

@admin.register(Unitofstudy)
class ModelAdmin(admin.ModelAdmin): pass

@admin.register(Reviews)
class ModelAdmin(admin.ModelAdmin): pass

@admin.register(Experience)
class ModelAdmin(admin.ModelAdmin): pass

@admin.register(Comments)
class ModelAdmin(admin.ModelAdmin): pass