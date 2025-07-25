from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import IndividualProfile, CorporateProfile, StudioProfile

HEAR_ABOUT_CHOICES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('friend', 'Friend'),
    ('other', 'Other'),
]

GOVERNORATE_CHOICES = [
    ('Cairo', 'Cairo'),
    ('Giza', 'Giza'),
    ('Alexandria', 'Alexandria'),
]

class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'required': True}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'required': True}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class IndividualRegistrationForm(BaseRegistrationForm):
    full_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(required=False)
    nationality = forms.CharField(required=False)
    governorate = forms.ChoiceField(required=False, choices=GOVERNORATE_CHOICES)
    city = forms.CharField(required=False)
    id_front = forms.FileField(required=False)
    id_back = forms.FileField(required=False)
    hear_about = forms.ChoiceField(required=False, choices=HEAR_ABOUT_CHOICES)
    agree_terms = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the terms.'})

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            IndividualProfile.objects.create(
                user=user,
                full_name=self.cleaned_data.get('full_name'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                phone_number=self.cleaned_data.get('phone_number'),
                nationality=self.cleaned_data.get('nationality'),
                governorate=self.cleaned_data.get('governorate'),
                city=self.cleaned_data.get('city'),
                id_front=self.cleaned_data.get('id_front'),
                id_back=self.cleaned_data.get('id_back'),
                hear_about=self.cleaned_data.get('hear_about'),
            )
        return user

class CorporateRegistrationForm(BaseRegistrationForm):
    company_name = forms.CharField(required=True)
    company_phone = forms.CharField(required=False)
    commercial_register = forms.FileField(required=False)
    tax_card = forms.FileField(required=False)
    website = forms.URLField(required=False)
    governorate = forms.ChoiceField(required=False, choices=GOVERNORATE_CHOICES)
    city = forms.CharField(required=False)
    hear_about = forms.ChoiceField(required=False, choices=HEAR_ABOUT_CHOICES)
    agree_terms = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the terms.'})

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            CorporateProfile.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                company_phone=self.cleaned_data.get('company_phone'),
                commercial_register=self.cleaned_data.get('commercial_register'),
                tax_card=self.cleaned_data.get('tax_card'),
                website=self.cleaned_data.get('website'),
                governorate=self.cleaned_data.get('governorate'),
                city=self.cleaned_data.get('city'),
                hear_about=self.cleaned_data.get('hear_about'),
            )
        return user

class StudioRegistrationForm(BaseRegistrationForm):
    studio_name = forms.CharField(required=True)
    studio_phone = forms.CharField(required=False)
    commercial_register = forms.FileField(required=False)
    tax_card = forms.FileField(required=False)
    governorate = forms.ChoiceField(required=False, choices=GOVERNORATE_CHOICES)
    city = forms.CharField(required=False)
    hear_about = forms.ChoiceField(required=False, choices=HEAR_ABOUT_CHOICES)
    agree_terms = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the terms.'})

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            StudioProfile.objects.create(
                user=user,
                studio_name=self.cleaned_data.get('studio_name'),
                studio_phone=self.cleaned_data.get('studio_phone'),
                commercial_register=self.cleaned_data.get('commercial_register'),
                tax_card=self.cleaned_data.get('tax_card'),
                governorate=self.cleaned_data.get('governorate'),
                city=self.cleaned_data.get('city'),
                hear_about=self.cleaned_data.get('hear_about'),
            )
        return user