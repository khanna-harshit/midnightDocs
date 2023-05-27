from django.contrib import admin

# Register your models here.
from .models import contact

from .models import appointment
from .models import image
from .models import blogpost

admin.site.register(appointment)
admin.site.register(contact)
admin.site.register(image)
admin.site.register(blogpost)
