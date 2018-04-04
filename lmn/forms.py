from django import forms
from .models import Note

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class VenueSearchForm(forms.Form): #creates class form with input restriction 
    search_name = forms.CharField(label='Venue Name', max_length=200)


class ArtistSearchForm(forms.Form): #creates class form with input restriction 
    search_name = forms.CharField(label='Artist Name', max_length=200)


class NewNoteForm(forms.ModelForm): #creates class form with input restriction 
    class Meta:
        model = Note
        fields = ('title', 'text')


class UserRegistrationForm(UserCreationForm):

    class Meta:#creates class form with input restriction 
        model = User  #this is the user. This is used to validate information
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def clean_username(self): #used to create username

        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('Please enter a username') #raises error if username is not valid

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists') #if this username exists already error is raised

        return username


    def clean_first_name(self): #validates first name
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('Please enter your first name')

        return first_name


    def clean_last_name(self): #validates last name
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError('Please enter your last name')

        return last_name


    def clean_email(self): #validates email
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Please enter an email address')

        if User.objects.filter(email__iexact=email).exists(): #checks to make sure there are no duplicates
            raise ValidationError('A user with that email address already exists')

        return email


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username'] #saves clean data
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save() #saves user info

        return user
