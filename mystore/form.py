from django import forms
from .models import Contact

class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField()
    message = forms.Textarea()

    class Meta:
        model = Contact
        fields = ['name','phone','email','message']