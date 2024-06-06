from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

import main.models as main_m


admin.site.register(main_m.Training)
admin.site.register(main_m.FinishedTraining)
admin.site.register(main_m.Exercise)
admin.site.register(main_m.FinishedExerciseSet)
admin.site.register(main_m.FinishedRunning)

@admin.register(main_m.CustomUser)
class UserAdmin(DjangoUserAdmin):
    """
    Admin panel for CustomUser model with no email field
    """

    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name',),
        }),
    )
    list_display = ('username', 'first_name', 'is_staff')
    search_fields = ('username', 'first_name')
    ordering = ('username',)
