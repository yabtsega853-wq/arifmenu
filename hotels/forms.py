from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hotel, MenuItem


class OwnerRegistrationForm(UserCreationForm):
    hotel_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=20)
    license_number = forms.CharField(required=False)
    verification_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Hotel.objects.create(
                owner=user,
                name=self.cleaned_data['hotel_name'],
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone'],
                license_number=self.cleaned_data.get('license_number', ''),
                verification_photo=self.cleaned_data.get('verification_photo')
            )
        return user


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price',
                  'category', 'image', 'available']
