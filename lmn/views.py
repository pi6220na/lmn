from django.shortcuts import render
from django.contrib.auth.models import User

def homepage(request):
    return render(request, 'lmn/home.html')

def logged_out(request):
    return render(request, 'lmn/logged_out.html')
# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     #user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#     user.save()