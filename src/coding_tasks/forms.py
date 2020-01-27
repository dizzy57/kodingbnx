from django.contrib.auth.forms import UserCreationForm


class CreateUserAndSetShortNameForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = user.username
        if commit:
            user.save()
        return user
