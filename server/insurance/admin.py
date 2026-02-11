from django.contrib import admin
from .models import Insurer, Agent, ServiceProvider, Surveyor, Policy

# Register your models here.

admin.site.register(Insurer)
admin.site.register(Agent)
admin.site.register(ServiceProvider)
admin.site.register(Surveyor)
admin.site.register(Policy)