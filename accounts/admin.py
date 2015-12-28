from django.contrib import admin
from django.contrib.auth.models import Group
from accounts.models import Account, UniversityGroup


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
                 ('Информация аккаунта', {'fields': ['username', 'password', 'is_active']}),
                 ('ФИО', {'fields': ['last_name', 'first_name', 'patronymic']}),
                 ('Информация о студенте', {'fields': ['universityGroup']}),
                 ('Права', {'fields': ['is_deanery', 'is_steward'], 'classes': ['collapse']})
                ]
    list_display = ('username', 'last_name', 'first_name', 'patronymic', 'universityGroup')
    list_display_links = ('username', 'first_name', 'last_name', 'patronymic')
    list_filter = [ 'universityGroup', 'is_active', 'is_steward', 'is_deanery']
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


class AccountInline(admin.StackedInline):
    model = Account
    fields = ['username',
              'password',
              'is_active',
              'last_name',
              'first_name',
              'patronymic',
              'universityGroup',
              'is_deanery',
              'is_steward'
             ]
    extra = 1


class UniversityGroupAdmin(admin.ModelAdmin):
    fields = ['name']
    inlines = [AccountInline]
    list_display = ['name']
    search_fields = ['name']
    ordering = ['-created_at']

admin.site.register(Account, AccountAdmin)
admin.site.register(UniversityGroup, UniversityGroupAdmin)
admin.site.unregister(Group)
