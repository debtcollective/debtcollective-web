from django.contrib import admin
from models import UserProfile, Debt, Point

class UserProfileAdmin(admin.ModelAdmin):
  exclude = ("user", )

class DebtAdmin(admin.ModelAdmin):
  exclude = ("UserProfile", )

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Debt, DebtAdmin)
admin.site.register(Point)