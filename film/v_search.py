from django.shortcuts import render_to_response
from models import *
import MySQLdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mylib import *
from myfunct import *
from classes import *
import v_IMDB, v_tmdb

@login_required(login_url='/accounts/login/')
def searchGlobal(request):
    search_s=None                    
                    
    #Risultati Form Ricerca
    if request.method == 'POST':
        search_s = request.POST.get('search')
        film_s = request.POST.get('film')
        director_s = request.POST.get('director')
        actor_s = request.POST.get('actor')
        genre_s = request.POST.get('genre')
        user_s = request.POST.get('user')
        group_s = request.POST.get('group')
        
    #Inizializzo Variabili
        film_db=None
        film_TMDB=None
        director_db=None
        actor_db=None
        genre_db=None
        user_db=None
        group_db=None
        
        
    #Ricerca nulla
    if search_s=='':
        none='Insert a valid search'
        return render_to_response('search.html', {'user': request.session['user'], 'img_prof': request.session['img_prof'], 'none': none})
    else:
        
        #RICERCA FILM IN DB E TMDB  (ritorna: film_db, film_TMDB)
        if film_s=='on':
            risultati = Film.objects.filter(titolo__icontains=search_s)            #cerco nel mio db
            film_db = pagination(request, risultati, 100)
            film_TMDB= v_tmdb.search_tmdb(search_s)
            film_TMDB = pagination(request, film_TMDB, 20)                          #cerco nel db di TMDB themoviedb.org
            
        #RICERCA REGISTI IN DB (ritorna: director_db)
        if director_s=='on':
            risultati = Regista.objects.filter(nome__icontains=search_s)
            director_db = pagination(request, risultati, 500)

        #RICERCA ATTORI IN DB (ritorna: actor_db)
        if actor_s=='on':
            risultati = Attore.objects.filter(nome__icontains=search_s)         
            actor_db = pagination(request, risultati, 500)
        
        #RICERCA GENERI IN DB (ritorna: actor_db)
        if genre_s=='on':
            risultati = Genere.objects.filter(descrizione__icontains=search_s)
            genre_db = pagination(request, risultati, 500)
            
        #RICERCA UTENTI IN DB (ritorna: user_db)
        if user_s=='on':
            user = get_user(request)
            query = User.objects.filter(username__icontains=search_s)
            query = query.exclude(is_superuser=1)
            query = query.exclude(id=user.id)
            user_db = pagination(request, query, 500)
            
        #RICERCA GRUPPI IN DB (ritorna: group_db)
        if group_s=='on':
            query = Group.objects.filter(name__icontains=search_s)
            group_db = pagination(request, query, 500)
            
            
    return render_to_response('search.html', {
                                              'user': request.session['user'], 
                                              'img_prof': request.session['img_prof'], 
                                              'search_s': search_s,
                                              'film_db': film_db,
                                              'film_TMDB': film_TMDB,
                                              'director_db': director_db,
                                              'actor_db': actor_db,
                                              'genre_db': genre_db,
                                              'user_db': user_db,
                                              'group_db': group_db
                                              }
                              )
    
