# importing the items need for the page
from django import forms
from .models import Note

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

# this class is for searching for venues
class VenueSearchForm(forms.Form):
    search_name = forms.CharField(label='Venue Name', max_length=200)

# this class if for searching for the artist
class ArtistSearchForm(forms.Form):
    search_name = forms.CharField(label='Artist Name', max_length=200)

# this class is for making a new note to post
class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text')

# This class is for creating a new user information
class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        # This function is to check for user name
    def clean_username(self):

        # this is to clean the input
        username = self.cleaned_data['username']

        # this happens if nothing entered
        if not username:
            raise ValidationError('Please enter a username')

            # this checks if the username already exist
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists')

        return username


        # This checks if there is something in the firstname
    def clean_first_name(self):
        # This is cleaning up the input
        first_name = self.cleaned_data['first_name']
        # This checks if something is in the first
        if not first_name:
            raise ValidationError('Please enter your first name')

        return first_name

        # this checks last name block
    def clean_last_name(self):
        # cleans up the input for the last name block
        last_name = self.cleaned_data['last_name']
        # if there is nothing in the last name block
        if not last_name:
            raise ValidationError('Please enter your last name')

        return last_name

        # checks the email block
    def clean_email(self):
        # cleans the input for email
        email = self.cleaned_data['email']
        # if not an email
        if not email:
            raise ValidationError('Please enter an email address')

            # if the email already exist in the db
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email address already exists')

        return email


        # function to save the information
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()

        return user
