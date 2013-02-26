from django.shortcuts import render_to_response
from models import *
import MySQLdb
from mylib import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from settings import *
from myfunct import *
from queries import *
from classes import *


@login_required(login_url='/accounts/login/')
def loggato(request):
    user = get_user(request)
    profile = Profilo.objects.get(user=user)

    return render_to_response('users/profile/logged.html', {'user': user, 'profile' : profile})