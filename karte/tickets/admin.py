from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.Movies),
admin.site.register(models.Ticket),

