# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # Add additional fields as required
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('location',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.location = self.cleaned_data['location']
        user.role = User.CUSTOMER
        status = ''
        if commit:
            if(user.location=='finland'):
                userExistency = list(User.objects.using('finland').filter(username=user.username).values())
                if(userExistency==[]):
                    userExistency = list(User.objects.using('sweden').filter(username=user.username).values())
                    if(userExistency==[]):
                        user.save(using=user.location)
                        user = list(User.objects.using(user.location).filter(username = user.username).values())[0]
                        del user['date_joined']
                        del user['last_login']
                    else:
                        status = 'A user with that username already exists'
                else:
                    status = 'A user with that username already exists'
            elif(user.location=='sweden'):
                userExistency = list(User.objects.using('sweden').filter(username=user.username).values())
                if(userExistency==[]):
                    userExistency = list(User.objects.using('finland').filter(username=user.username).values())
                    if(userExistency==[]):
                        user.save(using=user.location)
                        user = list(User.objects.using(user.location).filter(username = user.username).values())[0]
                        del user['date_joined']
                        del user['last_login']
                    else:
                        status = 'A user with that username already exists'
                else:
                    status = 'A user with that username already exists'
        return user,status       
