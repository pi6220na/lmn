from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

# to add a new note you must be logged in
@login_required
# function for adding a note
def new_note(request, show_pk):

    # there needs to be a show
    show = get_object_or_404(Show, pk=show_pk)


    if request.method == 'POST' :

        form = NewNoteForm(request.POST)
        if form.is_valid():

            # this is the form to use
            note = form.save(commit=False);
            if note.title and note.text:  # If note has both title and text
                note.user = request.user
                note.show = show
                note.posted_date = timezone.now()
                note.save()
                return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        # This makes a call to new note form
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form' : form , 'show':show })


# This calls the notes and puts them in order by posted date
def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date').reverse()
    return render(request, 'lmn/notes/note_list.html', {'notes':notes})

# This post note for a show by posted date
def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('posted_date').reverse()
    show = Show.objects.get(pk=show_pk)  # Contains artist, venue

    return render(request, 'lmn/notes/note_list.html', {'show': show, 'notes':notes } )


# This calls individual notes info
def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , {'note' : note })
