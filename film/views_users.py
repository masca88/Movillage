from django.shortcuts import render_to_response
from models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from mylib import *
from myfunct import *
from views_profile import *
from queries import *
from classes import *
from django.http import HttpResponseRedirect
import string
import random

#registrazione utenti
def register(request):

    presente = None                                          #inizializzazione
    completed = None
    fail = None
    username = None
    
    if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       password2 = request.POST.get('password2')
       email = request.POST.get('email')
       nome = request.POST.get('nome')
       cognome = request.POST.get('cognome')
       paese = request.POST.get('paese')
       citta = request.POST.get('citta')
       eta = request.POST.get('age')
       sex = request.POST.get('gender')

       presente = User.objects.filter(username=username)


       if (len(presente) == 0):
          if password == password2:                                 #se la password inserita coincide con la richiesta di conferma
             user = User.objects.create_user(username=username,email=email, password=password)     #inserimento dati
             user.is_staff = True
             user.is_active = False
             user.save()
             confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(30))
             userid = User.objects.get(username = username).id
             inserimento = Profilo(user=user, nome=nome, cognome=cognome, paese=paese, citta=citta, eta=eta, gender=sex, confirmation_code=confirmation_code)
             inserimento.save()
             send_registration_confirmation(user)
             completed = "An email was sent to your account, follow the instructions to activate your account."              #registrazione completata
             return render_to_response('registration/register.html', {
                                                                      'completed' : completed
                                                                      })

          else:
               if password != password2:                                                            #altrimenti manda gli opportuni messaggi di errore
                  fail = "Password didn't match...try again"
                  return render_to_response('registration/register.html', {
                  'completed' : completed, 'username' : username, 'fail' : fail})
       else:
            fail = "User already existing"
            return render_to_response('registration/register.html', {'fail' : fail})

    return render_to_response('registration/register.html', {'fail' : fail})


def send_registration_confirmation(user):
    user = User.objects.get(username=user)
    p = Profilo.objects.get(user=user)

    title = "Movillage account confirmation"
    content = "Hi " + p.nome + " " + p.cognome + ", \nwelcome in Movillage! \n\nClick on this link to activate your account: \n\n " + SITE_URL + "/confirm/" + str(p.confirmation_code) + "/" + user.username + "\n\n\n---\nMovillage STAFF"
    send_mail(title, content, 'no-reply@movillage.com', [user.email], fail_silently=False)

def confirm(request, confirmation_code, username):
    try:
        user = User.objects.get(username=username)
        profile = Profilo.objects.get(user=user)
        if profile.confirmation_code == confirmation_code:
            user.is_active = True
            user.save()
            alert="Thanks for your registration " + username + ", now you can login and try the Movillage experience!"
        return render_to_response('registration/confirm.html', {'completed' : alert})
    except:
        alert="Error!"
        return render_to_response('registration/confirm.html', {'completed' : alert})
    
    
#visualizzazione del profilo utente selezionato
@login_required(login_url='/accounts/login/')
def profilo(request, id, alert=None):

    io = get_user(request)
    notfriends = None
    user = User.objects.get(id=id)
    fri=1
    follower=None
    following=None
    
    giaamico = Amicizia.objects.filter(user=io.id, amico=id, confermata=1)
    giaamicoinv = Amicizia.objects.filter(user=id, amico=io.id, confermata = 1)
    giafollower= Follower.objects.filter(user_id=io.id, followed_id=id) 
    giafollowerinv= Follower.objects.filter(user_id=id, followed_id=io.id)
    
    if(io.id == user.id):
        return myprofile(request)
    if(len(giaamico) == 0 and len(giaamicoinv) == 0):
        fri=0
        
    if(len(giafollower) > 0):
        following=1
    
    if(len(giafollowerinv) > 0):    
        follower=1
        
        
        
    if(len(giaamico) == 0 and len(giaamicoinv) == 0 and follower!=1 and following!=1):
        notfriends = 1
        return render_to_response('users/profilo.html', {
                                                          'user': request.session['user'],
                                                          'img_prof': request.session['img_prof'],  
                                                          'notfriends' : user
                                                          })
        
    
    profile = Profilo.objects.get(user=id)
    if (profile.gender == 'm'):
        profile.gender = 'male'
    else:
        profile.gender = 'female'

    #AMICI
    risultati = []                                      #inizializzazione
    risultati = get_user_friends(request, user.id)
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
    listafilm = []
    risultati = []    
    pref = Preferito.objects.filter(utente=user.id).values('film').order_by('?')[:10]      #cerca i preferiti nella bd

    for j in pref:                                                     #elabora i risultati
        listafilm.append(j['film'])
    for i in listafilm:
        film = Film.objects.get(id=i)
        risultati.append(film)


    filmPref = pagination(request, risultati, 10)

    #GRUPPI
    query = 'SELECT * FROM auth_group, film_profilogruppo, auth_user where auth_user.id = film_profilogruppo.user_id AND auth_group.id = film_profilogruppo.group_id AND film_profilogruppo.user_id = %s'
    g_user = db_query_params(request, query, user.id)
    gruppi = pagination(request, g_user, 50)
    
    #GENERI PREFERITI
    query = 'select * from film_generepreferito inner join film_genere on film_genere.id = film_generepreferito.genere_id where user_id = %s ORDER BY RAND() limit 5'
    genres = db_query_params(request, query, user.id)

    #ATTORI PREFERITI
    query = 'select * from film_attorepreferito inner join film_attore on film_attore.id = film_attorepreferito.attore_id where user_id = %s ORDER BY RAND() limit 5'
    actors = db_query_params(request, query, user.id)
    
    #REGISTI PREFERITI
    query = 'select * from film_registapreferito inner join film_regista on film_regista.id = film_registapreferito.regista_id where user_id = %s ORDER BY RAND() limit 5'
    dirs = db_query_params(request, query, user.id)
    
    if(fri==1):
        return render_to_response('users/profilo.html', {'user': request.session['user'], 
                                                         'img_prof': request.session['img_prof'], 
                                                         'friend' : user,
                                                         'filmPref': filmPref, 
                                                         'postsg': gruppi, 
                                                         'profile' : profile,
                                                         'friends': friends,
                                                         'follow': follow,
                                                         'genres': genres,
                                                         'actors': actors,
                                                         'dirs': dirs,
                                                         'alert': alert
                                                        })
        
    if(fri==0 and following==1):
        return render_to_response('users/profilo.html', {'user': request.session['user'], 
                                                         'img_prof': request.session['img_prof'], 
                                                         'following' : user,
                                                         'filmPref': filmPref, 
                                                         'postsg': gruppi, 
                                                         'profile' : profile,
                                                         'genres': genres,
                                                         'actors': actors,
                                                         'dirs': dirs,
                                                         'alert': alert
                                                        })

    if(fri==0 and follower==1):
        return render_to_response('users/profilo.html', {'user': request.session['user'], 
                                                         'img_prof': request.session['img_prof'], 
                                                         'follower' : user,
                                                         'filmPref': filmPref, 
                                                         'postsg': gruppi, 
                                                         'profile' : profile,
                                                         'genres': genres,
                                                         'actors': actors,
                                                         'dirs': dirs,
                                                         'alert': alert
                                                        })
#richiesta di amicizia
@login_required(login_url='/accounts/login/')
def amicizia(request, id):

    conferma = None                           

    user = get_user(request)
    giaamico = Amicizia.objects.filter(user=user.id, amico=id, confermata=1)
    giaamicoinv = Amicizia.objects.filter(user=id, amico=user.id, confermata = 1)

    if (len(giaamico) != 0):    #se i due utenti sono gia amici
        alert = "Already friends"
        #return render_to_response('alert.html', {
        return profilo(request, id, alert)

    if (len(giaamicoinv) != 0):
        alert = "Already friends"
        return profilo(request, id, alert)


    presente = Amicizia.objects.filter(user=user.id, amico=id, confermata= 0)
    presenteinv = Amicizia.objects.filter(user=id, amico=user.id , confermata = 0)
    if (len(presente) == 0):
        if (len(presenteinv) == 0):                                                              #invia correttamente la richiesta di amicizia
            inserimento = Amicizia(user_id=user.id, amico_id=id)
            inserimento.save()
            conferma = "Friend request correctly sent"                                            #altrimenti manda opportuno messaggio di errore
        else:
            conferma = "This user has already posted you a friendship request"
    else:
        conferma = "You have already posted a friendship request to this user"

    return profilo(request, id, conferma)



#accetta l'amicizia
@login_required(login_url='/accounts/login/')
def conferma(request, amicizia):

    alert = None    

    a = Amicizia.objects.filter(id=amicizia).update(confermata=True)             #conferma l'amicizia
    a = Amicizia.objects.get(id=amicizia)
    alert = "You accepted a friendship request"
    return profilo(request, a.user_id, alert)

    

#rifiuta l'amicizia
@login_required(login_url='/accounts/login/')
def rifiuta(request, amicizia):

    conferma = None

    a = Amicizia.objects.filter(id=amicizia).delete()                            #rifiuta l'amicizia e cancella la tupla
    conferma = "You refused a friendship request"
    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'],
                                             'completed' : conferma
                                             })

#visualizza gli amici dell'utente loggato
@login_required(login_url='/accounts/login/')
def amici(request , id=None, alert=None):
    
    notfriends = None
    risultati = []                                      #inizializzazione
    risultati = get_friends(request , id)
    friends = pagination(request, risultati, 20)
    
    user = User.objects.get(id=id)


    return render_to_response('users/all_details.html', {'user': request.session['user'], 
                                                         'img_prof': request.session['img_prof'], 
                                                         'friends' : friends, 
                                                         'notfriends' : notfriends,
                                                         'rel':user,
                                                         'alert': alert
                                                         })
           




#cerca un utente nella bd
@login_required(login_url='/accounts/login/')
def selectUser(request):

    user = get_user(request)                  #inizializzazione
    posts = None
    query = None
    form = ricercaUtente(request.POST)

    adv_usr = advice_friend_profile(request) 
    adv_usr = pagination(request, adv_usr,  3)



    if form.is_valid():                       #estrazione dati da form

       u = form.cleaned_data['username']
       q = 'select * from auth_user, film_foto where auth_user.id = film_foto.user AND id <> %s and is_superuser <> 1 AND lower(username) LIKE %%s%'
       p = [user.id, u]
       query = User.objects.filter(username__icontains=u)
       query = query.exclude(is_superuser=1)
       query = query.exclude(id=user.id)

       if(len(query) == 0):
                     nouser = "No match found"
                     return render_to_response('alert.html', {'completed' : nouser})

       posts = pagination(request, query, 5) #effettua una query sulla bd

    else:
         form = ricercaUtente()
    return render_to_response('users/userSearch.html', {
    'form': form, 'adv_usr' : adv_usr, 'posts': posts})
    


def amiciUser(request, id):

    risultati = []                                      #inizializzazione

    user = get_user(request)
    notfriends = None
    risultati = get_user_friends(request, id)

    if(len(risultati) == 0):
                      notfriends = "This user hasn't added any other friends yet"
                      return render_to_response('alert.html', {'completed' : notfriends})
    posts = pagination(request, risultati, 5)


    return render_to_response('users/amiciUser.html', { 'posts' : posts, 'user' : user
           })




#cerca un utente nella bd
@login_required(login_url='/accounts/login/')
def filterUser(request):
    lista =[]
    posts = None
    user = get_user(request)                  #inizializzazione

    form = filtraUtente(request.POST)
    if form.is_valid():                       #estrazione dati da form
       adv_usr = advice_friend_profile2(request)
       c = form.cleaned_data['country']
       h = form.cleaned_data['hometown']
       s = form.cleaned_data['sex']

       if(c == ''):
            c = None
       if(h == ''):
            h = None
       if(s == ''):
            s = None

       if(c == None and h == None and s != None):               #001
            query = 'select * from auth_user, film_profilo where auth_user.id = film_profilo.user_id AND gender = %s'
            results = db_query_params(request, query, s)
            posts = pagination(request, results, 5)
            return render_to_response('users/userFilter.html', {'form': form, 'posts': posts})

       if(c == None and h != None and s == None):               #010
            query = 'select * from auth_user, film_profilo where auth_user.id = film_profilo.user_id AND citta = %s'
            results = db_query_params(request, query, h)
            posts = pagination(request, results, 5)
            return render_to_response('users/userFilter.html', {'form': form, 'posts': posts})

       if(c == None and h != None and s != None):                                                        #011
            PAR = [h, s]
            query = 'select * from auth_user, film_profilo where auth_user.id = film_profilo.user_id AND citta = %s AND gender = %s AND is_superuser = 0'
            results = db_query_params(request, query, PAR)
            posts = pagination(request, results, 5)
            return render_to_response('users/userFilter.html', {'form': form, 'posts': posts})

       if(c != None and h == None and s == None):                                                          #100
            query = 'select * from auth_user, film_profilo where auth_user.id = film_profilo.user_id AND paese = %s AND is_superuser = 0'
            results = db_query_params(request, query, c)
            posts = pagination(request, results, 5)
            return render_to_response('users/userFilter.html', {'form': form, 'posts': posts})

       if(c != None and h == None and s != None):                                                         #101
            PAR2 = [c, s]
            query = 'select * from auth_user, film_profilo where auth_user.id = film_profilo.user_id AND paese = %s AND gender = %s AND is_superuser = 0'
            results = db_query_params(request, query, PAR2)
            posts = pagination(request, results, 5)
            return render_to_response('users/userFilter.html', {'form': form, 'posts': posts})

       if(c != None and h != None and s == None):                                                         #110
            PAR3 = [c, h]
            query = 'select * from auth_user, film_profilo where auth_user.id = film_profilo.user_id AND paese = %s AND citta = %s AND is_superuser = 0'
            results = db_query_params(request, query, PAR3)
            posts = pagination(request, results, 5)
            return render_to_response('users/userFilter.html', {'form': form, 'posts': posts})

       if(c != None and h != None and s != None):                                                         #111
            PAR4 = [c, h, s]
            query = 'select * from auth_user, film_profilo where auth_user.id = film_profilo.user_id AND paese = %s AND citta= %s AND gender = %s AND is_superuser = 0'
            results = db_query_params(request, query, PAR4)
            posts = pagination(request, results, 5)
            return render_to_response('users/userFilter.html', {'form': form, 'posts': posts})

       posts = pagination(request, lista, 5)

    else:
         form = filtraUtente()
    return render_to_response('users/userFilter.html', {
                                                        'user': request.session['user'],
                                                        'img_prof': request.session['img_prof'],
                                                        'adv_usr': adv_usr,
                                                        'form': form, 
                                                        'posts': posts
                                                        })
