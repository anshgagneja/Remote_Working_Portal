from django.contrib import admin
from django.contrib.auth.models import Group
from student.models import MyUser, Assignment, Submission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# class UserCreationForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = MyUser
#         fields = ('email',)
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = MyUser
#         fields = ('email', 'password', 'is_active', 'teacher','student')
#
#     def clean_password(self):
#         return self.initial["password"]
#
#
# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#     list_display = ('email', )
#     list_filter = ('teacher',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('full_name',)}),
#         ('Permissions', {'fields': ('teacher',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['email','full_name','teacher','student']
admin.site.register(MyUser,MyUserAdmin)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.unregister(Group)
