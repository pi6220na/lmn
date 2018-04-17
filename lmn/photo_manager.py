import logging


# photo is an ImageFieldFile object which has a convenient delete() method
# from wishlist_with_uploads_for_app_engine
def delete_photo(photo):
    logging.info('to do : delete photo at url %s' % photo)
    photo.delete()
