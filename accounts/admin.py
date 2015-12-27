from django.contrib import admin
from django.contrib.auth.models import Group
from accounts.models import Account


class AccountAdmin(admin.ModelAdmin):
    fields = ['username',
              'password',
              'first_name',
              'last_name',
              'patronymic',
              'is_deanery',
              'is_steward',
              'is_active']
    list_display = ('__str__', 'username', 'first_name', 'last_name', 'patronymic')
    list_display_links = ('__str__', 'username', 'first_name', 'last_name', 'patronymic')
    list_filter = ['is_active', 'is_steward', 'is_deanery']
    search_fields = ['first_name', 'last_name', 'patronymic', 'username']
    ordering = ['-created_at']

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = Account.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()


admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)
