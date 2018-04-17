from django.contrib import admin

# Register your models here, for them to be displayed in the admin view

# getting the models for each part to be able to view and edit
from .models import Venue, Artist, Note, Show

# give the admin the ablity to work with these parts
admin.site.register(Venue)
admin.site.register(Artist)
admin.site.register(Note)
admin.site.register(Show)
