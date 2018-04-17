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
import io


def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    if hasattr(user, 'userinfo') and hasattr(user.userinfo, 'user_bio_info'):
        user_bio_info = user.userinfo.user_bio_info
    else:
        user_bio_info = 'Still a work in progress.'
    return render(request, 'lmn/users/user_profile.html', {'user' : user , 'notes' : usernotes , 'bio_info' : bio_info})

def user_profile_photo(request, user_pk):
    user = User.objects.get(pk=user_pk)
    userinfo = user.userinfo
    if userinfo is None:
        return Http404("No such photo.")

    user_photo= userinfo.user_photo
    return HttpResponse(user_photo)

@login_required
def edit_user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data["user_name", False]
            user.first_name = form.cleaned_data["user_first", False]
            user.last_name = form.cleaned_data["user_last", False]
            user.email = form.cleaned_data["user_email", False]
            user_bio_info=form.cleaned_data["user_bio_info", False]
            user_photo = request.FILES["user_photo", False]

            user.userinfo.user_bio_info = user_bio_info
            if hasattr(photo) and user_photo_file_name is not None:
                user.userinfo.user_photo_name = photo.name
                user.userinfo.user_photo = photo

            user.save()
            user.userinfo.save()

        if hasattr(user, 'userinfo') and user.userinfo is not None:
            user_bio_info = user.userinfo.user_bio_info
            photo = user.userinfo.user_photo
        else:
            user.userinfo = UserInfo()
            about_me = "Dancing to the music in my head"
            user.save()
            user.userinfo.save()

        user.save()
        user.userinfo.save()

    else:
        raise RuntimeError(form.errors)

    form = UserEditForm({"user_name": user.username,
                         "user_first": user.first_name,
                         "user_last": user.last_name,
                         "user_email": user.email,
                         "user_bio_info": user.user_bio_info,
                         "user_photo": user.photo})

    return render(request, 'lmn/users/edit_user_profile.html', {'form': form, 'user': user})



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
