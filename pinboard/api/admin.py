from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Pin)
admin.site.register(Board)
admin.site.register(Message)
admin.site.register(PinMessage)