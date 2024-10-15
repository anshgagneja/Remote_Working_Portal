from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from student.models import MyUser, Assignment, Submission

class SignupForm(UserCreationForm):
    choice = forms.ChoiceField(choices=[('student','student'),('teacher','teacher')])
    class Meta:
        model = MyUser
        fields = ["full_name","email","college_name","choice"]

class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields = ['username','password']


class AssignmentForm(ModelForm):
    upload = forms.FileField(
        required=False,
        label='Select a file',
        help_text='max.200 megabytes'
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )
    class Meta:
        model = Assignment
        fields = ["title","course_code","course_title","upload","due_date"]

class SubmissionForm(ModelForm):
    upload = forms.FileField(required=True)
    class Meta:
        model = Submission
        fields = ["assignment","upload","description","submitted_at"]


# class AssignmentSearchform(forms.Form):
#     q = forms.CharField()
#
#     class Meta:
#         model = Assignment
#         fields = ["q"]
#
# class SubmissionSearchForm(forms.Form):
#     q = forms.CharField()
#
#     class Meta:
#         fields = "q"




