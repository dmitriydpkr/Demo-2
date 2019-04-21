from django import forms
from .models import Order, Good
from django.core import validators


class OrderForm(forms.ModelForm):
    # убрать поле из формы. ForeignKey = ModelChoiceField
    good = forms.ModelChoiceField(queryset=Good.objects.all(), widget=forms.HiddenInput)
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Enter your email again !')
    text = forms.CharField(widget=forms.Textarea,
                           validators=[validators.MaxLengthValidator(200)])

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        vmail = cleaned_data['verify_email']

        if email != vmail:

            raise forms.ValidationError('Make sure email match')

        return cleaned_data

    class Meta:
        model = Order
        fields = ('good', 'name', 'phone', 'email', 'text')
    fields_order = ['good', 'name', 'phone', 'email', 'text']

