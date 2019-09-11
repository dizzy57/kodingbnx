from django import forms


class SubmitSolutionForm(forms.Form):
    url = forms.URLField(max_length=255)
