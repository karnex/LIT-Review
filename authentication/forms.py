from django import forms


class UsernameForm(forms.Form):
    username = forms.CharField(max_length=60, label='',
                               widget=forms.TextInput(attrs={'class': 'form-control text-center',
                                                             'placeholder': 'Nom d\'utilisateur'}))


class PasswordForm(forms.Form):
    password = forms.CharField(max_length=60, label='',
                               widget=forms.PasswordInput(attrs={'class': 'form-control text-center',
                                                                 'placeholder': 'Mot de passe'}))
