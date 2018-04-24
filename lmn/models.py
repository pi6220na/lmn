from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# code from tutorial: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

#Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False

'''A User Profile'''

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_bio_info = models.TextField(blank=True, max_length=1000)
    user_photo = models.BinaryField(null=True, blank=True)
    user_favorite_artist = models.CharField(max_length=200, blank=True)
    user_favorite_venue = models.CharField(max_length=200, blank=True)
    user_favorite_show = models.CharField(max_length=200, blank=True)

    def __str__(self):
        #return "Bio Information: My name is {} and {}.".format(self.user.first_name, self.user_bio_info)
        return "{} {} {} {} {} ".format(self.user_name, self.user_favorite_venue,
            self.user_favorite_artist, self.user_favorite_show, self.user_bio_info)


@receiver(post_save, sender=User)
def create_user_info(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    instance.userinfo.save()

''' A music artist '''
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False);
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return "Artist: " + self.name

    # def __str__(self):
    #     return 'Artist: %s\nPhoto %s' % (self.name, self.photo.url if self.photo else 'no photo')



''' A venue, that hosts shows. '''


class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False)  # What about international?
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return 'Venue name: {} in {}, {}\n{}'.format(self.name, self.city, self.state, self.photo.url if self.photo else 'no photo')


''' A show - one artist playing at one venue at a particular date. '''


class Show(models.Model):
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return 'Show with artist {} at {} on {}'.format(self.artist, self.venue, self.show_date)


''' One user's opinion of one show. '''
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False)

    def publish(self):
        posted_date = datetime.datetime.today()
        self.save()

    def __str__(self):
        return 'Note for user ID {} for show ID {} with title {} text {} posted on {}'.format(self.user, self.show, self.title, self.text, self.posted_date)
