from django.contrib import admin

# Register your models here.
from .models import Documents, InvertedIndex
admin.site.register(Documents)
admin.site.register(InvertedIndex)
