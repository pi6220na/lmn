from django import forms
from .models import Note, UserInfo

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class VenueSearchForm(forms.Form):
    search_name = forms.CharField(label='Venue Name', max_length=200)


class ArtistSearchForm(forms.Form):
    search_name = forms.CharField(label='Artist Name', max_length=200)


class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text')


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserEditForm(forms.ModelForm):

    user_favorite_venue = forms.CharField(label='Favorite Venue',required=False)
    user_favorite_artist = forms.CharField(label='Favorite Artist',required=False)
    user_favorite_show = forms.CharField(label='Favorite Show',required=False)
    user_bio_info = forms.CharField(label='Bio Information', widget=forms.Textarea, help_text='What was your most memorable experience with music?',required=False)
    user_photo = forms.ImageField(widget=forms.FileInput(attrs={"id": "id_file"}), label='User Photo', required=False)

     class Meta:
         model = UserInfo
         fields = ('user_favorite_venue', 'user_favorite_artist', 'user_favorite_show', 'user_bio_info', 'user_photo')
