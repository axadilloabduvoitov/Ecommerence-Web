from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from .models import Review


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "login",
            "placeholder": "Username kiriting",
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        label="Parol",
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "login",
            "placeholder": "Kamida 8 ta belgi",
            "autocomplete": "new-password",
        }),
    )
    captcha = CaptchaField(label="Tasdiqlash")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bu username allaqachon mavjud.")
        return username

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating' : forms.Select(attrs={'class' : 'form-control'}),
            'comment' : forms.Textarea(attrs={'class' : 'form-control',
            'placeholder' : 'Mahsulot haqida fikringiz ?' }),
        }