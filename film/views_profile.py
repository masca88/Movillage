from django.shortcuts import render_to_response, HttpResponse, RequestContext
from models import *
import MySQLdb
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from mylib import *
from django.core.files import File
from classes import *
from queries import get_friends
import re

@login_required(login_url='/accounts/login/')
def myprofile(request):
    user = get_user(request)
    profile = Profilo.objects.get(user=user)



    if (profile.gender == 'm'):
        sex = 'male'
    else:
        sex = 'female'

    #GRUPPI
    query = 'SELECT * FROM auth_group, film_profilogruppo, auth_user where auth_user.id = film_profilogruppo.user_id AND auth_group.id = film_profilogruppo.group_id AND film_profilogruppo.user_id = %s'
    g_user = db_query_params(request, query, user.id)
    postsg = pagination(request, g_user, 5)
    
    risultati = []                     #inizializzazione
    listafilm = []
    empty = None

    #AMICI
    risultati = []                                      #inizializzazione
    risultati = get_friends(request)
    friends = pagination(request, risultati, 5)
    
    #FOLLOW
    risultati = []
    query = 'select * from film_follower f, film_profilo p where f.user_id = %s and f.user_id = p.user_id'
    f = db_query_params(request, query, user.id)
    for i in f:
        u = Profilo.objects.get(user_id=i['followed_id'])
        risultati.append(u)
    follow = pagination(request, risultati, 5)

    #FILM PREFERITI
    risultati = []    
    idutente = request.session['user_id']
    pref = Preferito.objects.filter(utente=idutente).values('film').order_by('?')[:10]     #cerca i preferiti nella bd
    username = request.session['user']

    for j in pref:                                                     #elabora i risultati
        listafilm.append(j['film'])
    for i in listafilm:
        film = Film.objects.get(id=i)
        risultati.append(film)


    filmPref = pagination(request, risultati, 10)
    
    #GENERI PREFERITI
    query = 'select * from film_generepreferito inner join film_genere on film_genere.id = film_generepreferito.genere_id where user_id = %s ORDER BY RAND() limit 5'
    genres = db_query_params(request, query, idutente)

    #ATTORI PREFERITI
    query = 'select * from film_attorepreferito inner join film_attore on film_attore.id = film_attorepreferito.attore_id where user_id = %s ORDER BY RAND() limit 5'
    actors = db_query_params(request, query, idutente)
    
    #REGISTI PREFERITI
    query = 'select * from film_registapreferito inner join film_regista on film_regista.id = film_registapreferito.regista_id where user_id = %s ORDER BY RAND() limit 5'
    dirs = db_query_params(request, query, idutente)
    
    return render_to_response('users/profile/myprofile.html', {
                                                               'user': request.session['user'],
                                                               'img_prof': request.session['img_prof'], 
                                                               'profile' : profile, 
                                                               'postsg' : postsg, 
                                                               'sex' : sex, 
                                                               'friends': friends,
                                                               'follow': follow,
                                                               'filmPref': filmPref,
                                                               'genres': genres,
                                                               'actors': actors,
                                                               'dirs':dirs                                                               
                                                               })


@login_required(login_url='/accounts/login/')
#registrazione utenti
def change_passwd(request):
    alert = None
    user = get_user(request)

    if request.method == 'POST':                             #estrazione dati dal form
       form = ch_pass(request.POST)
       if form.is_valid():
          old_p = form.cleaned_data['old_password']
          new_p = form.cleaned_data['new_password']
          new_pc = form.cleaned_data['new_password_conf']

          if (user.check_password(old_p) == True):
             if new_p == new_pc:                                 #se la password inserita coincide con la richiesta di conferma
                user.set_password(new_p)
                user.save()
                alert = "Your password has been changed!"              #registrazione completata
                return render_to_response('users/profile/change_passwd.html', {
                                                                   'user': request.session['user'],
                                                                   'img_prof': request.session['img_prof'], 
                                                                   'alert' : alert,
                                                                   'form': form
                                                                   })
             else:
                  if new_p != new_pc:                                                                 #altrimenti manda gli opportuni messaggi di errore
                     alert = "Try again"
                     form = ch_pass()
          else:
                alert = "Your old password is incorrect, try again!!!"
                form = ch_pass()
    else:
         form = ch_pass()
    return render_to_response('users/profile/change_passwd.html', {
                                                                   'user': request.session['user'],
                                                                   'img_prof': request.session['img_prof'], 
                                                                   'alert' : alert,
                                                                   'form': form
                                                                   })        
    
    


from django.core.files.move import file_move_safe

@login_required(login_url='/accounts/login/')
def upload_image(request):
    '''Simple view method for uploading an image
 
    '''  
    fil = None
    alert = None
    user = get_user(request)
    fil = user.username
    fil += '.'
    
    if request.method == 'POST':

        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['image']._get_name()
            img = re.sub('^.*\.', fil , img )
            inserimento = Profilo.objects.filter(user=user.id).update(name=img)
            save_file(img , request.FILES['image'])
            alert = "Photo profile uploaded"
            return render_to_response('users/profile/photo_profile.html', {
                                                                           'user': request.session['user'],
                                                                           'img_prof': request.session['img_prof'], 
                                                                           'alert' : alert,
                                                                           'form': form
                                                                           })
        else:
            alert = "Error .. try again"
            return render_to_response('users/profile/photo_profile.html', {
                                                                           'user': request.session['user'],
                                                                           'img_prof': request.session['img_prof'], 
                                                                           'alert' : alert,
                                                                           'form': form
                                                                           })
    else:
        form = ImageForm()
    return render_to_response('users/profile/photo_profile.html', {
                                                                   'user': request.session['user'],
                                                                   'img_prof': request.session['img_prof'], 
                                                                   'form': form
                                                                   })
 
 
def save_file(filename, file , path=MEDIA_ROOT + MEDIA_URL):
    ''' Little helper to save a file
    '''   
    
    fd = open('%s/%s' % ('', str(path) + str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()