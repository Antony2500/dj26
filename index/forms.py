import datetime
import re

from django import forms
from django.forms import modelform_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Stuff, Product, Book

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a data between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data["renewal_date"]

        if data < datetime.date.today():
            raise ValidationError('Invalid date - renewal in past')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError("Invalid date - renewal more than 4 weeks ahead")

        return data


class StuffForm(forms.ModelForm):
    class Meta:
        model = Stuff
        fields = "__all__"
        # fields = ["stuff_name", "price"]


class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


BookForm = forms.modelform_factory(
    Product,
    fields=("title", "price"),
    widgets={"title": forms.widgets.Textarea()}
)

class CreateProduct(UserCreationForm):
    class Meta:
        model = Product
        fields = "__all__"


class BookForm2(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"


    def clean_code(self):
        code = self.cleaned_data.get("code")
        pattern = r"^A.{4,}$"
        if not re.match(pattern, code):
            raise ValidationError("Code must start with 'A' and be at least 5 characters long")
        return code