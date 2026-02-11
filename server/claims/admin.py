from django.contrib import admin
from .models import Claim, InspectionReport, Settlements

# Register your models here.

admin.site.register(Claim)
admin.site.register(InspectionReport)
admin.site.register(Settlements)