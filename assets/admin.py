from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Asset, AssetClass, Domain, Attribute


admin.site.register(Asset)
admin.site.register(AssetClass)
admin.site.register(Attribute)
admin.site.register(Domain)
