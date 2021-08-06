from django.contrib import admin

# Register your models here.

from group.models import Group, Join, JoinRequest

admin.site.register(Group)
admin.site.register(Join)
admin.site.register(JoinRequest)