from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from app.lmn.lmn.models import Artist, Venue, User
import logging
from django.core.files.storage import default_storage


# from wishlist_with_uploads_for_app_engine
@receiver(post_delete, sender=Artist)
def place_post_delete_image_cleanup(sender, **kwargs):

    # kwargs['instance'] is the deleted Place object.
    # The Place object has been deleted from the DB,
    # but the Python Place object still exists, with data in its fields.
    logging.info('post delete hook')
    artist = kwargs['instance']
    if artist.photo:
        logging.info(artist.photo)
        if default_storage.exists(artist.photo.name):
            default_storage.delete(artist.photo.name)


@receiver(post_save, sender=Artist)
def place_pre_save_image_cleanup(sender, **kwargs):

    # kwargs['instance'] is the Place object, about to be updated
    new_artist = kwargs['instance']
    # Can use this to get pk and query DB for previous values
    # Filter by pk and take first item
    old_artist = Artist.objects.filter(pk=new_artist.pk).first()
    # If there's already a place with this pk - so this save is for an update - then
    # check to see if there is a photo, and if so, delete it
    if old_artist and old_artist.photo:
        if default_storage.exists(old_artist.photo.name):
            logging.info('delete', old_artist.photo.name)
            default_storage.delete(old_artist.photo.name)


# from wishlist_with_uploads_for_app_engine
@receiver(post_delete, sender=Venue)
def place_post_delete_image_cleanup(sender, **kwargs):

    # kwargs['instance'] is the deleted Place object.
    # The Place object has been deleted from the DB,
    # but the Python Place object still exists, with data in its fields.
    logging.info('post delete hook')
    venue = kwargs['instance']
    if venue.photo:
        logging.info(venue.photo)
        if default_storage.exists(venue.photo.name):
            default_storage.delete(venue.photo.name)


@receiver(pre_save, sender=Venue)
def place_pre_save_image_cleanup(sender, **kwargs):

    # kwargs['instance'] is the Place object, about to be updated
    new_venue = kwargs['instance']
    # Can use this to get pk and query DB for previous values
    # Filter by pk and take first item
    old_venue = Venue.objects.filter(pk=new_venue.pk).first()
    # If there's already a place with this pk - so this save is for an update - then
    # check to see if there is a photo, and if so, delete it
    if old_venue and old_venue.photo:
        if default_storage.exists(old_venue.photo.name):
            logging.info('delete', old_venue.photo.name)
            default_storage.delete(old_venue.photo.name)
