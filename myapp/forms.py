from django import forms
from django.contrib.auth.models import User
from .models import TrainingApplication


class TrainingApplicationForm(forms.ModelForm):
    # Explicitly enforce file-upload validation on the form level
    student_passport = forms.ImageField(required=True)
    guardian_passport = forms.ImageField(required=True)

    class Meta:
        model = TrainingApplication
        fields = [
            "surname",
            "first_name",
            "middle_name",
            "address",
            "age",
            "phone_number",
            "level_of_education",
            "program",
            "duration",
            "start_date",
            "end_date",
            "guardian_name",
            "guardian_address",
            "guardian_phone_number",
            "student_passport",
            "guardian_passport",
        ]

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data