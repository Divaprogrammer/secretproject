from django.contrib import admin
from .models import Reactions,Comments
# Register your models here.
admin.site.register((Reactions,Comments))