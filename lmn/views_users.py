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

@login_required
def edit_user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data.get("user_name", False)
            user.first_name = form.cleaned_data.get("first_name", False)
            user.last_name = form.cleaned_data.get("last_name", False)
            user.email = form.cleaned_data.get("email", False)
            user.favorite_venue = form.cleaned_data.get("favorite_venue", False)
            user.favorite_artist = form.cleaned_data.get("favorite_artist", False)
            user.favorite_show = form.cleaned_data.get("favorite_show", False)
            user.user_bio_info = form.cleaned_data.get("user_bio_info", False)
            #user.user_profile_photo = request.FILES.get["user_profile_photo"]
            user.save()
            user.user_profile.save()

    else:
        form = UserEditForm({"user_name": user.username,
                             "user_first": user.first_name,
                             "user_last": user.last_name,
                             "user_email": user.email,})
                             #"favorite_venue": user.favorite_venue,
                             #"favorite_artist": user.favorite_artist,
                             #"favorite_show": user.favorite_show,
                             #"user_bio_info": user.user_bio_info})

    return render(request, 'lmn/users/edit_user_profile.html', {'form': form, 'user' : user})



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
