from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response, redirect
from models import *
import MySQLdb
from mylib import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from settings import *
from myfunct import *
from queries import *
from classes import *
from models import *
from django.contrib.auth.views import logout_then_login


def login_h(request): 
    #LAST FILMS ADDED
    lastadded = get_lastadded(request)
    lastadded = pagination(request,lastadded, 10)
    mostfollowed = get_mostfollowed(request)
    mostfollowed = pagination(request,mostfollowed, 5)
    
    adv_film_wri = None
    adv_film_reg = None
    adv_friend = None

    user=0
    try:
        user= get_user(request)
    except:
        user=0
    if user is 0:
        #LOGGIN'
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            err= ''
            
            if user is not None:
                if user.is_active:
                    login(request, user)         # Session user started.
                    profile=Profilo.objects.get(user=user)
                    request.session ['user']=user
                    request.session ['user_id']=profile.user_id
                    request.session ['img_prof']=profile.name
                    nfollow = Follower.objects.filter(followed = user).count()
                    richieste = Amicizia.objects.filter(amico = user.id, confermata = False)           #cerca se ci sono richieste di amicizia non confermate
                    
                    
                    try:
                        '''
                        adv_film_wri = advice_wri(request)
                        adv_film_reg = advice_reg(request)
                        if(adv_film_reg != None):
                            if(adv_film_wri != None):
                                adv_film_wri = adv_film_wri + adv_film_reg
                            else:
                                adv_film_wri =adv_film_reg
                        if(adv_film_wri != None):
                            adv_film_wri = elimina_doppioni(request, adv_film_wri)
                            adv_film_wri = pagination(request, adv_film_wri, 6)
                        '''           
                    
                        commenti = get_notify(request)
                        commenti = pagination(request,commenti, 5)
                        gr_iscriz = get_iscrizioni(request)
                        
                        '''
                        adv_friend = adv_user_genre(request)
                        adv_friend = pagination(request,adv_friend, 4)
                        '''
                    except: # A user with the e-mail provided was not found
                        return redirect('accounts/login/')
                else:   
                    err= 'disabled account'      # Return a 'disabled account' error message
                    return render_to_response('home/login.html', {'err': err, 'lastadded': lastadded})

            else:
                err= 'Incorrect Username or Password'               # Return an 'invalid login' error message.
                return render_to_response('home/login.html', {'err': err, 'lastadded': lastadded})
    
            return render_to_response('home/logged.html', {
                                                           'user': request.session['user'],
                                                           'img_prof': request.session ['img_prof'],
                                                           'user': profile,  
                                                           'lastadded': lastadded, 
                                                           'mostfollowed': mostfollowed, 
                                                           'richieste': richieste, 
                                                           'nfollow': nfollow, 
                                                           #'adv_film': adv_film_wri, 
                                                           #'adv_friend': adv_friend, 
                                                           'commenti': commenti, 
                                                           'gr_iscriz': gr_iscriz
                                                           })
            
        else:        
            return render_to_response('home/login.html', {'lastadded': lastadded })
    else:
        user=get_user(request)
        nfollow = Follower.objects.filter(followed = user).count()
        richieste = Amicizia.objects.filter(amico = user.id, confermata = False)           #cerca se ci sono richieste di amicizia non confermate
        commenti = get_notify(request)
        commenti = pagination(request,commenti, 5)
        gr_iscriz = get_iscrizioni(request)
        
        '''
        adv_friend = adv_user_genre(request)
        adv_friend = pagination(request,adv_friend, 4)
        adv_film_wri = advice_wri(request)
        adv_film_reg = advice_reg(request)
        if(adv_film_reg != None):
            if(adv_film_wri != None):
                adv_film_wri = adv_film_wri + adv_film_reg
            else:
                adv_film_wri =adv_film_reg
        if(adv_film_wri != None):
                        adv_film_wri = elimina_doppioni(request, adv_film_wri)
                        adv_film_wri = pagination(request, adv_film_wri, 6)
        '''
               
        return render_to_response('home/logged.html', {'user': request.session['user'], 
                                                       'lastadded': lastadded,
                                                       'user': user, 
                                                       'mostfollowed': mostfollowed, 
                                                       'img_prof': request.session['img_prof'],
                                                       'richieste': richieste, 'nfollow': nfollow, 
                                                       #'adv_film': adv_film_wri, 
                                                       #'adv_friend': adv_friend, 
                                                       'commenti': commenti, 
                                                       'gr_iscriz': gr_iscriz
                                                       })

@login_required(login_url='/accounts/login/')
def logout_h(request):
    return logout_then_login(request, login_url='/')
    