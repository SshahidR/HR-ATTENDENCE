from django import forms
from django.contrib.auth.forms import UserChangeForm
# from django.contrib.auth.models import User
from .models import CustomUser
from hr.utils import activate_user



class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'is_active' in self.changed_data and user.is_active:
            # Trigger email notification only if is_active is being updated to True
            
            activate_user(None, user.id)  # Pass None for request as it's not used in the view
        if commit:
            user.save()
        return user
    



class CustomForm(forms.Form):
    status = forms.CharField()
    message = forms.CharField()
    subject = forms.CharField()



from .models import userAttendance

class UserAttendanceSearchForm(forms.ModelForm):
    class Meta:
        model = userAttendance
        fields = ['username', 'status', 'start_date', 'end_date']

    username = forms.CharField(required=False)
    status = forms.CharField(required=False)
    start_date = forms.DateField(required=False, label='From Date')
    end_date = forms.DateField(required=False, label='To Date')
    search_button = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=True)  # Hidden field to indicate search
