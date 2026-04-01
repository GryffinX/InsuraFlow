from django.contrib import admin
from .models import Provider, Agent, ServiceProvider, Surveyor, Policy, UserPolicy

# Register your models here.

admin.site.register(Provider)
admin.site.register(Agent)
admin.site.register(ServiceProvider)
admin.site.register(Surveyor)
admin.site.register(Policy)
admin.site.register(UserPolicy)
