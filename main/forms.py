from django import forms
from .models import Person, Address, Advertisement, Sales, CustomUser, Phone, Mobile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "person_type",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-group"
            else:
                field.widget.attrs["class"] = "form-control form-group"


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["city", "neighborhood", "state"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-group"
            else:
                field.widget.attrs["class"] = "form-control form-group"


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["person", "title", "site", "price", "fonte"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-group"
            else:
                field.widget.attrs["class"] = "form-control form-group"


class PersonUpdateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "email",
            "person_type",
            "status",
            "funnel_stage",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-group"
            else:
                field.widget.attrs["class"] = "form-control form-group"


class AdvertisementUpdateForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ["title", "site", "price",]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                if field.widget.attrs.get("class"):
                    field.widget.attrs["class"] += " form-control form-group"
                else:
                    field.widget.attrs["class"] = "form-control form-group"


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-group"
            else:
                field.widget.attrs["class"] = "form-control form-group"


class CustomAuthenticationForm(AuthenticationForm):
    # Se você quiser adicionar campos personalizados ao formulário de login, faça aqui
    pass


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ["telefone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-group"
            else:
                field.widget.attrs["class"] = "form-control form-group"


class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = ["celular"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                field.widget.attrs["class"] += " form-control form-group"
            else:
                field.widget.attrs["class"] = "form-control form-group"
