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


def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    bio_info = user.userinfo.user_bio_info if user.userinfo else "YO"
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
            user.username = form.cleaned_data["user_name"]
            user.first_name = form.cleaned_data["user_first"]
            user.last_name = form.cleaned_data["user_last"]
            user.email = form.cleaned_data["user_email"]
            user_bio_info=form.cleaned_data["user_bio_info"]
            user_photo = request.FILES["user_photo"]

            if user.userinfo is None:
                user.userinfo = UserInfo()

            user.userinfo.user_bio_info = user_bio_info
            #user.userinfo.user_photo_name = photo.name
            #user.userinfo.user_photo = photo.read()

            user.save()
            user.userinfo.save()
        else:
            raise RuntimeError(form.errors)

    uinfo = user.userinfo
    if uinfo:
        user_bio_info = uinfo.user_bio_info
        #photo = uinfo.user_photo
    else:
        user_bio_info = "I dance to the music in my head!"
        photo = None

    form = UserEditForm({"user_name": user.username,
                         "user_first": user.first_name,
                         "user_last": user.last_name,
                         "user_email": user.email,
                         "user_bio_info": user_bio_info,
                         "user_photo": photo})

    return redirect('lmn:user_profile', user_pk=request.user.pk)



def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
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
    return render(request, 'registration/logout.html', {'message':message})
