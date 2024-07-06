from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Visitor, Report
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'phone_number', 'user_type')
    list_filter = ('email',)
    # fieldsets = (
    #     (None, {'fields': ('email', 'username', 'password')}),
    #     ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser')}),
    # )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_type')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('id', 'visitor_name', 'visitor_email', 'get_location', 'purpose')
    search_fields = ('visitor_name', 'visitor_email',)
    ordering = ('visitor_name', 'visitor_email')

    def get_location(self, obj):
        return f'{obj.latitude}, {obj.longitude}'

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_creator', 'created_at')
    search_fields = ('title', 'creator_id')
    ordering = ('title', 'creator_id')

    def get_creator(self, obj):
        if obj.creator_type == 'user':
            # Fetch the user object if it's a user
            try:
                user = User.objects.get(id=obj.creator_id)
                return user.username
            except User.DoesNotExist:
                return 'Unknown User'
        else:
            # Otherwise, return the visitor name
            return obj.creator_id

    get_creator.short_description = 'Creator'

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Report, ReportAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
