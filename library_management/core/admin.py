from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Books,LibraryUsers

admin.site.register(Books)
admin.site.register(LibraryUsers)