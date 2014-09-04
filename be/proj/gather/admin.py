from django.contrib import admin
from models import UserData, Debt

class UserDataAdmin(admin.ModelAdmin):
  exclude = ("user_id_secret", )

class DebtAdmin(admin.ModelAdmin):
  exclude = ("userdata", )

admin.site.register(UserData, UserDataAdmin)
admin.site.register(Debt, DebtAdmin)
