from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Products, Books, Phones

class CustomUserCreationForm(UserCreationForm):
    is_seller = forms.BooleanField(required=False, label="Do you like to sell items as well?")

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'is_seller']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'stock', 'image']

class BookForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Books
        fields = ProductForm.Meta.fields + ['pages', 'author']

class PhoneForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Phones
        fields = ProductForm.Meta.fields + ['brand']