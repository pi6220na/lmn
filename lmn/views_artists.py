from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm
import webbrowser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

# this getting the venues the artist has played a show
def venues_for_artist(request, artist_pk):   # pk = artist_pk

    ''' Get all of the venues where this artist has played a show '''

    shows = Show.objects.filter(artist=artist_pk).order_by('show_date').reverse() # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    return render(request, 'lmn/venues/venue_list_for_artist.html', {'artist' : artist, 'shows' :shows})

# this gets the artist list is searched for or artist link
def artist_list(request):
    form = ArtistSearchForm()
    # this is used if a search is conducted
    search_name = request.GET.get('search_name')
    # If a search is made
    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')
        # if it is linked into
    else:
        artists = Artist.objects.all().order_by('name')

    return render(request, 'lmn/artists/artist_list.html', {'artists':artists, 'form':form, 'search_term':search_name})

# Give the details on the artist
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk);
    return render(request, 'lmn/artists/artist_detail.html' , {'artist' : artist})
