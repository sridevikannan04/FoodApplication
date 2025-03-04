from django import forms
from django.contrib.auth.models import User
from .models import Role,FoodItems

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[("Buyer", "Buyer"), ("Seller", "Seller")])


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItems
        fields = ['name', 'description', 'price', 'image']
