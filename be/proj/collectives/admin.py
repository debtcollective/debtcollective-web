from django.contrib import admin
from proj.collectives.models import UserAction, Action, Collective

# Register your models here.
class ActionAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}

class CollectiveAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}

admin.site.register(UserAction)
admin.site.register(Action, ActionAdmin)
admin.site.register(Collective, CollectiveAdmin)
