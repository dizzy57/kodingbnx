from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput, ModelForm

from coding_tasks.models import Profile


class CreateUserAndSetShortNameForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = user.username
        if commit:
            user.save()
        return user


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name"]
        labels = {"first_name": "Display name"}


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["away_until"]
        widgets = {"away_until": DateInput(attrs={"type": "date"})}
