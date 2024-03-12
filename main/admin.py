from django.contrib import admin
from .models import Address, Advertisement, Person, Sales, CustomUser, Phone, Mobile

admin.site.register(Address)
admin.site.register(Advertisement)
admin.site.register(Person)
admin.site.register(Sales)
admin.site.register(CustomUser)
admin.site.register(Phone)
admin.site.register(Mobile)
