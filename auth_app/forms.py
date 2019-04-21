from django.contrib.auth.models import User
from django import forms
from main_app.models import Good
from .models import Comment


class UserForm(forms.ModelForm):
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter your email again !')
    password = forms.CharField(widget=forms.PasswordInput)
    verify_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        vmail = cleaned_data['verify_email']
        password = cleaned_data['password']
        verify_pass = cleaned_data['verify_password']

        if email != vmail and password != verify_pass:
            raise forms.ValidationError('Make sure email and password match')
        del cleaned_data['verify_email']
        del cleaned_data['verify_password']
        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', )


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ('name', 'images', 'brand')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_overview',)


