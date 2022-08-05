from django.contrib.auth.forms import UserCreationForm, UserChangeForm,  PasswordChangeForm, SetPasswordForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, Permission
from crispy_forms.layout import Layout, Row, Column, Submit, Button, HTML, Hidden, Div, Field
from crispy_forms.helper import FormHelper
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from accounts.models import Account

class CreateUserForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ['full_name', 'email','phone_number', 'password1', 'password2']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ['full_name', 'email', 'phone_number', 'password','is_active']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.fields['password'].help_text = self.fields['password'].help_text.replace(
            '../', '')
        
class UserSetPasswordForm(SetPasswordForm):
    class Meta:
        field = '__all__'
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Save', css_class='btn-success'))
    helper.form_method = 'POST'