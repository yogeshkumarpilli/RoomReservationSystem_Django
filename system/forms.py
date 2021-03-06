from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Reservation, Room
from bootstrap_datepicker_plus import DatePickerInput

# This  Class is for User Registeration Form
class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=False, label=('First name'))
    last_name = forms.CharField(max_length=30, required=False, label=('Last name'))
    email = forms.EmailField(label=('Email'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# This Class is for User Upgradation Form
class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(max_length=30, required=False, label=('First name'))
    last_name = forms.CharField(max_length=30, required=False, label=('Last name'))
    email = forms.EmailField(label=('Email'))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

# This  Class is for User Update Registeration Form
class CreateUpdateReservation(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['date', 'room', 'comment']

        labels = {
            'room': 'Room',
            'comment': 'Comment',
            forms.DateTimeField(): 'Date',
        }

        widgets = {
            'date': DatePickerInput()
        }

# This is for User Modification Form
class CreateModifyRoom(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['name', 'capacity', 'projector']

        labels = {
            'name': 'Name',
            'capacity': 'Capacity',
            forms.BooleanField(help_text='Projector'): 'Projector',
        }