from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import User

class RegistrationForm(UserCreationForm):
    business_name = forms.CharField(
        max_length=255, 
        required=True, 
        label="Business Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your shop or company name'})
    )
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'OWNER'  # Default role for new registrations
        if commit:
            user.save()
        return user
