from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404
from models import *
import MySQLdb
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.conf import settings
from mylib import *
from classes import *
from tmdb3 import *

#inserimento di un film nei preferiti
@login_required(login_url='/accounts/login/')
def insPreferiti(request, film):

    conferma = "This film has already been inserted"                                   #inizializzazione
    idutente = get_user(request)
    username = idutente.username
    idfilm = film
    presente = Preferito.objects.filter(utente=idutente.id, film=idfilm)

    if(len(presente) == 0):
                     inserimento = Preferito(film_id=idfilm, utente_id=idutente.id)
                     inserimento.save()
                     conferma = "Film correctly inserted"
                     return scheda(request, idfilm, conferma)

    return scheda(request, idfilm, conferma)

@login_required(login_url='/accounts/login/')
def insFavGen(request, genre):

    conferma = "This genre has already been inserted"                                   #inizializzazione
    user = get_user(request)
    username = user.username


    presente = GenerePreferito.objects.filter(user=user.id, genere=genre)

    if(len(presente) == 0):
                     inserimento = GenerePreferito(genere_id=genre, user_id=user.id)
                     inserimento.save()
                     conferma = "Genre correctly inserted into favourites"
                     return render_to_response('alert.html', {
                                                              'user': request.session['user'],
                                                              'img_prof': request.session['img_prof'], 
                                                              'completed' : conferma
                                                              })

    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'], 
                                             'completed' : conferma
                                             })
    
    
@login_required(login_url='/accounts/login/')
def insFavAct(request, actor):

    conferma = "This actor has already been inserted"                                   #inizializzazione
    user = get_user(request)
    username = user.username


    presente = AttorePreferito.objects.filter(user=user.id, attore=actor)

    if(len(presente) == 0):
                     inserimento = AttorePreferito(attore_id=actor, user_id=user.id)
                     inserimento.save()
                     conferma = "Actor correctly inserted into favourites"
                     return render_to_response('alert.html', {
                                                              'user': request.session['user'],
                                                              'img_prof': request.session['img_prof'], 
                                                              'completed' : conferma
                                                              })

    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'], 
                                             'completed' : conferma
                                             })


@login_required(login_url='/accounts/login/')
def insFavDir(request, director):

    conferma = "This director has already been inserted"                                   #inizializzazione
    user = get_user(request)
    username = user.username


    presente = RegistaPreferito.objects.filter(user=user.id, regista=director)

    if(len(presente) == 0):
                     inserimento = RegistaPreferito(regista_id=director, user_id=user.id)
                     inserimento.save()
                     conferma = "Director correctly inserted into favourites"
                     return render_to_response('alert.html', {
                                                              'user': request.session['user'],
                                                              'img_prof': request.session['img_prof'], 
                                                              'completed' : conferma
                                                              })

    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'], 
                                             'completed' : conferma
                                             })



#mostra preferiti utente loggato
@login_required(login_url='/accounts/login/')
def showPreferiti(request , id=None):
    
    risultati = []                     #inizializzazione
    listafilm = []
    empty = None

    userid = id
    pref = Preferito.objects.filter(utente=userid).values('film')     #cerca i preferiti nella bd

    for j in pref:                                                     #elabora i risultati
        listafilm.append(j['film'])
    for i in listafilm:
        film = Film.objects.get(id=i)
        risultati.append(film)


    movies = pagination(request, risultati, 20)
    user = User.objects.get(id=id)
    
    if(len(pref) == 0):
        empty = "You haven't inserted any film yet"
        return render_to_response('alert.html', {'completed' : empty})

    return render_to_response('users/all_details.html', {
                                                         'user': request.session['user'],
                                                         'img_prof': request.session['img_prof'], 
                                                         'movies': movies,
                                                         'rel': user
                                                         })
@login_required(login_url='/accounts/login/')
def showPref(request , id=None):
    userid = id
    
    user = User.objects.get(id=id)
    
    query = 'select * from film_generepreferito inner join film_genere on film_genere.id = film_generepreferito.genere_id where user_id = %s order by(descrizione)'
    genres = db_query_params(request, query, userid)
    
    query = 'select * from film_attorepreferito inner join film_attore on film_attore.id = film_attorepreferito.attore_id where user_id = %s order by(nome)'
    actors = db_query_params(request, query, userid)
    
    query = 'select * from film_registapreferito inner join film_regista on film_regista.id = film_registapreferito.regista_id where user_id = %s order by(nome)'
    dirs = db_query_params(request, query, userid)

    return render_to_response('users/all_details.html', {'user': request.session['user'],
                                                         'img_prof': request.session['img_prof'], 
                                                         'genres': genres,
                                                         'actors': actors,
                                                         'dirs': dirs,
                                                         'rel': user
                                                         })

@login_required(login_url='/accounts/login/')
def scheda(request, id, alert=''):

    somma = 0                                         #inizializzazione
    form = rate(request.POST)
    cast = []
    genere = []
    regia = []
    scrive = []
    set = []
    compagnia = []
    rating = None
    lang = []

    #estrae tutti i dati
    film = Film.objects.get(id=id)                                                #film
    filmcas = Filmcast.objects.filter(film=id).values('attore')                   #cast
    filmgen = GenereFilm.objects.filter(film=id).values('genere')                 #genere
    filmreg = Regia.objects.filter(film=id).values('regista')                     #registi
    filmscr = Scrive.objects.filter(film=id).values('scrittore')                  #scrittori
    filmlang = LinguaFilm.objects.filter(film=id).values('lingua')                #lingue
    filmset = Set.objects.filter(film=id).values('paese')                         #sets
    #filmcomp = CompagniaFilm.objects.filter(film=id).values('compagnia')          #compagnie
    filmrat = Voto.objects.filter(film=id)                                        #voti utenti
    
    
    for i in filmrat:
        somma = somma + i.rating
    for i in filmcas:
        result = Attore.objects.get(id=i['attore'])
        cast.append(result)
    for i in filmgen:
        result = Genere.objects.get(id=i['genere'])
        genere.append(result)
    for i in filmreg:
        result = Regista.objects.get(id=i['regista'])
        regia.append(result)
    for i in filmscr:
        result = Scrittore.objects.get(id=i['scrittore'])
        scrive.append(result)
    for i in filmlang:
        result = Lingua.objects.get(id=i['lingua'])
        lang.append(result)
    """
    for i in filmcomp:
        result = Compagnia.objects.get(id=i['compagnia'])
        compagnia.append(result)
    """
    for i in filmset:
        result = Paese.objects.get(id=i['paese'])
        set.append(result)
        
    if(filmrat.count() != 0):
        rating = somma / filmrat.count()                    #calcola la media dei voti e il numero degli utenti che hanno votato
        
    # Formatto il Cast 
    """ 
    listacast = []
    c = filmcast()
    comparsa = Compare.objects.filter(film=id).values('attore', 'personaggio')         #seleziona il ruolo

    for i in comparsa:
        act = Attore.objects.get(id=i['attore']).nome                                   #attore
        pers = Personaggio.objects.get(id=i['personaggio']).descrizione                 #personaggio
        c = filmcast()
        c.attore = act
        c.personaggio = pers
        listacast.append(c)
    
    cast = pagination(request, listacast, 50)
    """
    
    
    
    query = 'select film_commento.id as commento_id, film_commento.commento, film_profilo.name, auth_user.username, auth_user.id, film_commento.date from film_commento, film_profilo, auth_user where auth_user.id = film_profilo.user_id AND film_profilo.user_id = film_commento.utente_id AND film_id = %s ORDER by film_commento.date DESC'
    comments = db_query_params(request, query,id)
    comments = pagination(request, comments, 40)

    compagnia = pagination(request, compagnia, 100)
    return render_to_response('film/dettagli.html', {
                                                    'user': request.session['user'],
                                                    'img_prof': request.session['img_prof'],
                                                    'cast': cast, 
                                                    'genere': genere,
                                                    'regia' : regia,
                                                    'scrive' : scrive,
                                                    'lang' : lang,  
                                                   #'compagnia' : compagnia,  
                                                    'set' : set, 
                                                    'film' : film, 
                                                    'form' : form, 
                                                    'rating': rating, 
                                                    'nvoti' : filmrat.count(),
                                                    'comments': comments,
                                                    'alert': alert
                                                    })
 

#mostra il cast del relativo film col ruolo di ciascun attore
@login_required(login_url='/accounts/login/')
def cast(request, id):

    listacast = []
    c = filmcast()

    film = Film.objects.get(id=id)
    comparsa = Compare.objects.filter(film=id).values('attore', 'personaggio')         #seleziona il ruolo

    for i in comparsa:
        act = Attore.objects.get(id=i['attore']).nome                                   #attore
        pers = Personaggio.objects.get(id=i['personaggio']).descrizione                 #personaggio
        c = filmcast()
        c.attore = act
        c.personaggio = pers
        listacast.append(c)
    
    posts = pagination(request, listacast, 5)

    return render_to_response('film/cast.html', {
     'film' : film, 'posts' : posts})
    
    
@login_required(login_url='/accounts/login/')
def schedaimdb(request, id):
    risultati =  None
    creator = []
    ia = IMDb()
    risultati = ia.get_movie(id)
    for i in risultati['created by']:
        creator.append(i)
    return render_to_response('complete.html', {'film' : film, 'creator' : creator })
    

#inserimento rating
@login_required(login_url='/accounts/login/')
def rating(request, film):
    try:
        conferma = "You have already insert a reating"              #inizializzazione
        voto = request.POST['voto']
        idutente = get_user(request)
        idfilm = film
    
        presente = Voto.objects.filter(utente=idutente.id, film=idfilm)           #se l'utente ha gia inserito un rating per questo film
        if(len(presente) == 0):
            inserimento = Voto(film_id=idfilm, utente_id=idutente.id, rating=voto)
            inserimento.save()
            conferma = "Rating inserted"               #inserisce il rating
    except:
        conferma = "Select a rating"               #inserisce il rating

    return scheda(request, film, conferma)


#inserisce un commento su un film
@login_required(login_url='/accounts/login/')
def inserisciCommento(request, id):

    commentato = None                                          #inizializzazione
    form = None
    risultati = None
    username = None
    user = get_user(request)
    

    query = 'select film_commento.id as commento_id, film_commento.commento, film_profilo.name, auth_user.username, auth_user.id, film_commento.date from film_commento, film_profilo, auth_user where auth_user.id = film_profilo.user_id AND film_profilo.user_id = film_commento.utente_id AND film_id = %s ORDER by film_commento.date DESC'
    risultati = db_query_params(request, query,id)
    #risultati = Commento.objects.filter(film=id).order_by("date")      #seleziona tutti i commenti

    posts = pagination(request, risultati, 5)
    form = formCommento(request.POST)
    if form.is_valid():
       idutente = get_user(request)
       commento = form.cleaned_data['commento']                         #estrae i dati
       import textwrap
       commento = textwrap.fill(commento)
       username = idutente.username                                     #inserisce il commento
       inserimento = Commento(film_id=id, utente_id=idutente.id, commento=commento)
       inserimento.save()
       form = formCommento()
       commentato = 1
       conferma='Comment inserted'
    else:
         form = formCommento()
         conferma = 'Insert a Comment'
         
    #return render_to_response('film/dettagli.html', {
     #      'film' : id, 'posts': posts,'username' : username, 'form' : form, 'commentato' : commentato})
     
    return scheda(request, id, conferma) 
           
           
           
           
@login_required(login_url='/accounts/login/')
def report(request, id):
    conferma = None
    a = Commento.objects.filter(id=id).update(reported=True)             #conferma l'amicizia
    conferma = "You have reported this comment"
    return render_to_response('alert.html', {'completed' : conferma})

