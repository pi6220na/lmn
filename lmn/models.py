from django.db import models
from django.contrib.auth.models import User
import datetime
from PIL import Image

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

#Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False

# a class model for artists
''' A music artist '''
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

    # string constructor
    def __str__(self):
        return "Artist: " + self.name

    # def __str__(self):
    #     return 'Artist: %s\nPhoto %s' % (self.name, self.photo.url if self.photo else 'no photo')


# model for venues
''' A venue, that hosts shows. '''


class Venue(models.Model):
    # setting up the input info name unique, all have max charaters
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False)  # What about international?
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

    # String constructor
    def __str__(self):
        return 'Venue name: {} in {}, {}\n{}'.format(self.name, self.city, self.state, self.photo.url if self.photo else 'no photo')


''' A show - one artist playing at one venue at a particular date. '''

# model for shows
class Show(models.Model):
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    # String constructor
    def __str__(self):
        return 'Show with artist {} at {} on {}'.format(self.artist, self.venue, self.show_date)

# model for notes
''' One user's opinion of one show. '''
class Note(models.Model):
    # setting up the input info for db
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False)

    # function for post date of note
    def publish(self):
        posted_date = datetime.datetime.today()
        self.save()

        # String constructor
    def __str__(self):
        return 'Note for user ID {} for show ID {} with title {} text {} posted on {}'.format(self.user, self.show, self.title, self.text, self.posted_date)
