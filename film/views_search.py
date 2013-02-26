from django.shortcuts import render_to_response
from models import *
import MySQLdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mylib import *
from myfunct import *
from classes import *

#ricerca film nella bd o in IMDb
@login_required(login_url='/accounts/login/')
def selectFilm(request):
                                                                    #inizializzazione
    posts =  None
    query = None
    adv_film_wri = None
    adv_film_reg = None
    

    adv_film_wri = advice_wri(request)
    adv_film_reg = advice_reg(request)
    if(adv_film_reg != None):
                    if(adv_film_wri != None):
                                    adv_film_wri = adv_film_wri + adv_film_reg
                    else:
                        adv_film_wri =adv_film_reg
    if(adv_film_wri != None):
                    elimina_doppioni(request, adv_film_wri)
                    adv_film_wri = pagination(request, adv_film_wri, 7)



    form = ricercaFilm(request.POST)
    if form.is_valid():
        t = form.cleaned_data['film']                                #estrazione dati da form
        risultati = Film.objects.filter(titolo__icontains=t)         #cerca il film nella bd
        posts = pagination(request, risultati, 5)
        ia = IMDb()
        query = ia.search_movie(t, 6)                               #cerca film in IMDb
    else:
        form = ricercaFilm()
    return render_to_response('imdb/query.html', {
    'form': form, 'adv_film' : adv_film_wri,
    'posts': posts,'query': query})
    
    


#ricerca registi nella bd o in IMDb
@login_required(login_url='/accounts/login/')
def selectDir(request):
    search = 1                                                                #inizializzazione
    adv_film_reg = None
    posts =  None
    noresults = None
    formd = ricercaDir(request.POST)

    adv_film_reg = advice_reg(request)
    if(adv_film_reg != None):
                    elimina_doppioni(request, adv_film_reg)
                    adv_film_reg = pagination(request, adv_film_reg, 7)

    if formd.is_valid():
        d = formd.cleaned_data['director']                                #estrazione dati da form
        query = 'select * from film_regista where nome LIKE %s'
        risultati = db_query_params(request, query, d)
        if(len(risultati) == 0):
            noresults = "No match found, please search film by title"
            return render_to_response('imdb/queryDir.html', {'form': formd, 'search' : search, 'noresults' : noresults})
        posts = pagination(request, risultati, 5)
    else:
        formd = ricercaDir()
    return render_to_response('imdb/queryDir.html', {'form': formd, 'posts': posts, 'search' : search,'adv_film' : adv_film_reg, 'noresults' : noresults})
    
 







#ricerca film nella bd o in IMDb
@login_required(login_url='/accounts/login/')
def selectGen(request):
    search = 1                                                                  #inizializzazione
    posts =  None
    noresults = None
    adv_film_gen = advice_genre(request)
    if(adv_film_gen != None):
                    elimina_doppioni(request, adv_film_gen)
                    adv_film_gen = pagination(request, adv_film_gen, 7)

    formg = ricercaGen(request.POST)
    if formg.is_valid():
       d = formg.cleaned_data['genere']                                #estrazione dati da form
       query = 'select * from film_genere where descrizione LIKE %s'
       risultati = db_query_params(request, query, d)
       posts = pagination(request, risultati, 5)
       if(len(risultati) == 0):
                         noresults = "No match found, please search film by title"
                         return render_to_response('imdb/queryGen.html', {
                         'form': formg, 'search' : search, 'noresults' : noresults})

       return render_to_response('imdb/queryGen.html', {
       'form': formg,
       'posts': posts, 'search' : search,'adv_film' : adv_film_gen, 'noresults' : noresults})

    else:
         formg = ricercaGen()
    return render_to_response('imdb/queryGen.html', {
    'form': formg,
    'posts': posts, 'search' : search,'adv_film' : adv_film_gen, 'noresults' : noresults})
    
    





#ricerca film nella bd o in IMDb
@login_required(login_url='/accounts/login/')
def selectAct(request):
    search = 1                                                                  #inizializzazione
    posts =  None
    noresults = None

    adv_film_cast = advice_cast(request)
    if(adv_film_cast != None):
                    elimina_doppioni(request, adv_film_cast)
                    adv_film_cast = pagination(request, adv_film_cast, 7)

    formg = ricercaAct(request.POST)
    if formg.is_valid():
       d = formg.cleaned_data['actor']                                #estrazione dati da form
       query = 'select * from film_attore where nome LIKE %s'


       risultati = Attore.objects.filter(nome__icontains=d)         #cerca il film nella bd
       posts = pagination(request, risultati, 10)

       if(len(risultati) == 0):
                         noresults = "No match found, please search film by title"
                         return render_to_response('imdb/queryAct.html', {
                         'form': formg, 'search' : search, 'noresults' : noresults})


    else:
         formg = ricercaAct()
    return render_to_response('imdb/queryAct.html', {
    'form': formg,
    'posts': posts, 'search' : search,'adv_film' : adv_film_cast,  'noresults' : noresults})
    
    
def filmGen(request, id):
    query = None                                                                #inizializzazione
    posts =  None
    query = 'select * from film_film, film_generefilm where film_film.id = film_generefilm.film_id AND film_generefilm.genere_id = %s'
    movies = db_query_params(request, query, id)
    movies = pagination(request, movies, 20)
    gen = Genere.objects.get(id=id)
    type='genre'

    return render_to_response('linkedFilm.html',{
                                                 'user': request.session['user'],
                                                 'img_prof': request.session['img_prof'],
                                                 'movies': movies,
                                                 'rel':gen,
                                                 'type':type
                                                })    
    
def filmDir(request, id):
    query = None                                                                #inizializzazione
    posts =  None
    query = 'select * from film_film, film_regia where film_film.id = film_regia.film_id AND film_regia.regista_id = %s'
    movies = db_query_params(request, query, id)
    movies = pagination(request, movies, 20)
    dir = Regista.objects.get(id=id)
    type='dir'

    return render_to_response('linkedFilm.html',{
                                                 'user': request.session['user'],
                                                 'img_prof': request.session['img_prof'],
                                                 'movies': movies,
                                                 'rel':dir,
                                                 'type':type
                                                })

def filmAct(request, id):
    query = None                                                                #inizializzazione
    posts =  None
    query = 'select * from film_film, film_filmcast where film_film.id = film_filmcast.film_id AND film_filmcast.attore_id = %s'
    movies = db_query_params(request, query, id)
    movies = pagination(request, movies, 20)
    act = Attore.objects.get(id=id)
    type='actor'

    return render_to_response('linkedFilm.html',{
                                                 'user': request.session['user'],
                                                 'img_prof': request.session['img_prof'],
                                                 'movies': movies,
                                                 'rel': act,
                                                 'type':type
                                                })
