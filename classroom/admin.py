from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Note, Assignment

admin.site.register(Note)
admin.site.register(Assignment)