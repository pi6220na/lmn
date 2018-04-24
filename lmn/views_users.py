from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show, UserInfo
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserEditForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db import transaction
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, Http404
from PIL import Image

from django.db.models.signals import post_save
from django.forms import ValidationError
from django.contrib import messages
from django.db import transaction

def user_profile(request, user_pk):
        user = User.objects.get(pk=user_pk)
        usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
        return render(request, 'lmn/users/user_profile.html', {'user' : user , 'notes' : usernotes })

def user_profile_photo(request, user_pk):
    user = User.objects.get(pk=user_pk)
    userinfo = user.userinfo
    if userinfo is None:
        return Http404("No such photo.")

    user_photo= userinfo.user_photo
    return HttpResponse(user_photo)

#@login_required
#@transaction.atomic
def edit_user_profile(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        edit_user_form = UserEditForm(request.POST, instance=request.user.userinfo)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('lmn/users/edit_user_profile.html', user_pk=request.user.pk)
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserRegistrationForm(instance=request.user)
        edit_user_form = UserEditForm(instance=request.user.userinfo)
    return render(request, 'lmn/users/edit_user_profile.html', {
        'user_form': user_form,
        'profile_form': edit_user_form
    })

def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            user_info = UserInfo()
            user_info.user = user
            user_info.save()

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
