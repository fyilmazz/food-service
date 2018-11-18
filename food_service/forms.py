from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    address = forms.CharField(max_length=500, required=True, help_text="Zorunlu.")
    phone_number = forms.CharField(min_length=11, max_length=11, required=True, help_text="Zorunlu.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = "Zorunlu. 50 karakter ya da daha az olmalı. Sadece harfler, rakamlar ve @/./+/-/_ karakterleri kullanılabilir."
