import urllib2
from django import forms
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from models import *
import MySQLdb
from mylib import *
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from datetime import datetime, date
from settings import *
from myfunct import *
from views_followers import allFollow
from views_users import amici


@login_required(login_url='/accounts/login/')
def delete_friend(request, id):
    completed = None
    amicizia = None
    user = get_user(request)
    try:
        amicizia = Amicizia.objects.get(user = user, amico = id).delete()
        completed = "Friend correctly removed"
    except:
           amicizia = Amicizia.objects.get(user = id, amico = user).delete()
           completed = "Friend correctly removed"

    return amici(request, user.id, completed)



@login_required(login_url='/accounts/login/')
def delete_follow(request, id):
    completed = None
    follow = None
    user = get_user(request)
        
    follow = Follower.objects.get(user = user, followed = id).delete()
    completed = "Follow correctly removed"
    
    return allFollow(request, user.id, completed)


@login_required(login_url='/accounts/login/')
def delete_fav(request, id):
    user = get_user(request)
    fav = Preferito.objects.get(utente = user, film = id).delete()
    completed = "Film correctly removed from favourites"

    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'], 
                                             'completed' : completed
                                             })
    
    
    
@login_required(login_url='/accounts/login/')
def delete_sub(request, id):
    user = get_user(request)

    iscr = Iscrizione.objects.get(user = user, group = id).delete()
    completed = "Subcription correctly removed"

    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'], 
                                             'completed' : completed
                                             })
    
    
    
@login_required(login_url='/accounts/login/')
def delete_group(request, id):
    user = get_user(request)
    profilo = ProfiloGruppo.objects.get(group = id).delete()
    iscr = Iscrizione.objects.filter(group = id).delete()
    group = Group.objects.get(id = id).delete()
    completed = "Group correctly removed"

    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'], 
                                             'completed' : completed
                                             })
