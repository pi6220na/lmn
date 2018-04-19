from django.shortcuts import render, redirect, get_object_or_404
from django.conf.urls import url
from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, ArtistDetailForm
import webbrowser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .photo_manager import delete_photo

from django.utils import timezone


def venues_for_artist(request, artist_pk):   # pk = artist_pk

    ''' Get all of the venues where this artist has played a show '''

    shows = Show.objects.filter(artist=artist_pk).order_by('show_date').reverse() # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    return render(request, 'lmn/venues/venue_list_for_artist.html', {'artist' : artist, 'shows' :shows})


def artist_list(request):
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')
    else:
        artists = Artist.objects.all().order_by('name')

    return render(request, 'lmn/artists/artist_list.html', {'artists':artists, 'form':form, 'search_term':search_name})


def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    # return render(request, 'artists/artist_detail.html', {'artist': artist})

    if request.method == 'POST':

        # get a copy of the object so have a reference to the old photo,
        # just in case it needs to be deleted; user saves new photo or clears old one.
        old_artist = get_object_or_404(Artist, pk=artist_pk)

        form = ArtistDetailForm(request.POST, request.FILES, instance=place)  # instance = model object to update with the form data
        if form.is_valid():

            # If there was a photo added or removed, delete any old photo
            if 'photo' in form.changed_data:
                delete_photo(old_artist.photo)

            form.save()

            messages.info(request, 'Artist info updated')

        else:
            messages.error(request, form.errors)  # This looks hacky, replace

        return redirect('place_details', artist_pk=artist_pk)

    else:    # GET artist details  #from wishlist_with_uploads_for_app...
        review_form = ArtistDetailForm(instance=artist)  # Pre-populate with data from this Artist instance
        return render(request, 'lmn/artists/artist_detail.html', {'artist' : artist})

