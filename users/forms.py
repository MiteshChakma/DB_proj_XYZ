# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # Add additional fields as required
    location = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('location',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.location = self.cleaned_data['location']
        if commit:
            user.save()
        return user
