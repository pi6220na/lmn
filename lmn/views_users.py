from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show, UserInfo
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserEditForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, Http404
from PIL import Image

from django.db.models.signals import post_save
from django.forms import ValidationError
from django.contrib import messages
from django.db import transaction

def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if hasattr(user, 'userinfo') and hasattr(user.userinfo, 'user_bio_info'):
        user_bio_info = user.userinfo.user_bio_info
    else:
        user_bio_info = 'Still a work in progress.'
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    return render(request, 'lmn/users/user_profile.html', {'user' : user , 'bio_info' : user_bio_info, 'notes' : usernotes })

def user_profile_photo(request, user_pk):
    user = User.objects.get(pk=user_pk)
    userinfo = user.userinfo
    if userinfo is None:
        return Http404("No such photo.")

    user_photo= userinfo.user_photo
    return HttpResponse(user_photo)

#@login_required
#@transaction.atomic
def edit_user_profile(request, user_pk):

    if request.method == 'POST':
        #user_form = UserRegistrationForm(request.POST, instance=request.user)
        form = UserEditForm(request.POST, instance=request.user.userinfo)
        #print('user form is valid: ' + str(user_form.is_valid()))
        #print(user_form.errors)
        print('profile form is valid: ' + str(form.is_valid()))
        print(form.errors)
        if form.is_valid():# and profile_form.is_valid():
            print('in user form about to save')
            form.favorite_venue = form.cleaned_data.get("user_favorite_venue", False)
            form.favorite_artist = form.cleaned_data.get("user_favorite_artist", False)
            form.favorite_show = form.cleaned_data.get("user_favorite_show", False)
            form.user_bio_info = form.cleaned_data.get("user_bio_info", False)
            #form.user_photo = request.FILES.get["user_profile_photo"]
            form.save()
          #  profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            # return redirect('settings:profile')
            return redirect('lmn:edit_user_profile', user_pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        #user_form = UserRegistrationForm(instance=request.user)
        print(user_pk)
        form = UserEditForm(instance=request.user.userinfo)
        #form = UserEditForm()

        print(request.user.userinfo)
        print(request)

    return render(request, 'lmn/users/edit_user_profile.html', {
        #'user_form': user_form
        'form': form
    })

    # user = UserInfo.objects.get(user_name_id=user_pk)
    #
    # if request.method == 'POST':
    #
    #
    #
    #     form = UserEditForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         user = User.objects.get(pk=user_pk)
    #         user.favorite_venue = form.cleaned_data.get("user_favorite_venue", False)
    #         user.favorite_artist = form.cleaned_data.get("user_favorite_artist", False)
    #         user.favorite_show = form.cleaned_data.get("user_favorite_show", False)
    #         user.user_bio_info = form.cleaned_data.get("user_bio_info", False)
    #         #user.user_profile_photo = request.FILES.get["user_profile_photo"]
    #         print("saving user profile info")
    #         print(user)
    #
    #         user.save()
    #
    #
    #
    # else:
    #     form = UserEditForm({"user_name_id": user.user_name_id,
    #                          "favorite_venue": user.user_favorite_venue,
    #                          "favorite_artist": user.user_favorite_artist,
    #                          "favorite_show": user.user_favorite_show,
    #                          "user_bio_info": user.user_bio_info})
    #     #form = UserEditForm(empty_permitted=True)
    #
    # return render(request, 'lmn/users/edit_user_profile.html', {'form': form, 'user' : user})



def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            authenticate(username=request.POST['username'], password=request.POST['password1'])
            user = form.save()
            login(request, user)
            # user_info = UserInfo()
            # user_info.user = user
            # user_info.save()

            return redirect('lmn:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )


def logout_view(request):
    response = logout(request)
    message = 'You have been logged out\n Goodbye!'
    return render(request, 'registration/logout.html', {'message': message })



# the following code moved here from forms.py
def clean_username(self):

    username = self.cleaned_data['username']

    if not username:
        raise ValidationError('Please enter a username')

    if User.objects.filter(username__iexact=username).exists():
        raise ValidationError('A user with that username already exists')

    return username


def clean_first_name(self):
    first_name = self.cleaned_data['first_name']
    if not first_name:
        raise ValidationError('Please enter your first name')

    return first_name


def clean_last_name(self):
    last_name = self.cleaned_data['last_name']
    if not last_name:
        raise ValidationError('Please enter your last name')

    return last_name


def clean_email(self):
    email = self.cleaned_data['email']
    if not email:
        raise ValidationError('Please enter an email address')

    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError('A user with that email address already exists')

    return email


def save(self, commit=True):
    user = super(UserRegistrationForm, self).save(commit=False)
    user.username = self.cleaned_data['username']
    user.email = self.cleaned_data['email']
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']

    if commit:
        user.save()

    return user
