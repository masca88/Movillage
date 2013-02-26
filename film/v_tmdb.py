from django.shortcuts import render_to_response
import urllib
import json
from classes import *
from models import *
from django.contrib.auth.decorators import login_required
import re
from views_film import scheda
from queries import get_filmID
import tmdb
from settings import TMDB_KEY
from tmdb3 import *


#MOVIES SEARCH
def search_tmdb(title):
    tmdb.configure(TMDB_KEY)
    movie = tmdb.Movies(title,limit=True)
    
    filmList=[]
    
    try:
        for i in movie.iter_results():
            year = re.sub('-.*', '', i['release_date'])                         
            filmList.append(ricerca_TMDB(i['title'], year, i['id'], i['poster_path']))
        
    except:
        filmList = []
    
    return filmList

#NON IN USO
def search_tmdb3(title):
    set_key(TMDB_KEY)
    movie = searchMovie(title)
    
    filmList=[]
    
    try:
        for i in movie:
            filmList.append(ricerca_TMDB(i.title, Movie(i.id).releasedate.year, i.imdb, Movie(i.id).poster.filename))
        
    except:
        filmList = []
    
    return filmList
    
#TMDB UPLOAD
def insert_tmdb(request, id):
    set_key(TMDB_KEY)
    movie = Movie(id)
    
    presente=0
    presente = Film.objects.filter(imdbId__iexact=movie.imdb)
    conferma= "Film already existing"
    
    if(len(presente) != 0): 
        filmID=get_filmID(request, movie.imdb)
    
    if(len(presente) == 0):       
        title = movie.title
        plot = movie.overview
        poster = movie.poster.filename
        r_date = movie.releasedate.year
        imdbID = movie.imdb
        try:
            trailer = movie.youtube_trailers[0].source
            trailer = re.sub('&.*', '', trailer)                         
        except:
            trailer = ''

        
        film = Film(titolo = title, trama = plot, cover = poster, imdbId = imdbID, trailer=trailer, anno = r_date)  #film
        film.save()
        filmID = Film.objects.order_by('id').reverse()[0].id
    
        #Splitto le stringhe multiple e le inserisco nel DB
        i=0
        for i in movie.cast:
            pres = Attore.objects.filter(nome__iexact=i.name)
            if(len(pres) > 0):
                actID = Attore.objects.get(nome__iexact=i.name).id
                
            if(len(pres) == 0):
                insert = Attore(nome=i.name)
                insert.save()
                actID = Attore.objects.order_by('id').reverse()[0].id
                
            insert=0    
            insert = Filmcast(film_id=filmID, attore_id=actID)
            insert.save()
            
 
        i=0
        for i in movie.crew:
            if i.job == 'Director':
                pres = Regista.objects.filter(nome__iexact=i.name)
                if(len(pres) > 0):
                    dirID = Regista.objects.get(nome__iexact=i.name).id   
                    
                if(len(pres) == 0):
                    insert = Regista(nome=i.name)
                    insert.save()      
                    dirID = Regista.objects.order_by('id').reverse()[0].id
                    
                insert = Regia(film_id=filmID, regista_id=dirID)
                insert.save()
                
                
            if i.job == 'Author':
                pres = Scrittore.objects.filter(nome__iexact=i.name)
                if(len(pres) > 0):
                    wriID = Scrittore.objects.get(nome__iexact=i.name).id
                
                if(len(pres) == 0):
                    insert = Scrittore(nome=i.name)
                    insert.save()
                    wriID = Scrittore.objects.order_by('id').reverse()[0].id
                    
                insert = Scrive(film_id=filmID, scrittore_id=wriID)
                insert.save() 
            
        for i in movie.genres:                    
            pres = Genere.objects.filter(descrizione__iexact=i.name)
            if(len(pres) > 0):
                genID = Genere.objects.get(descrizione__iexact=i.name).id
                
            if(len(pres) == 0):
                insert = Genere(descrizione=i.name)
                insert.save()
                genID = Genere.objects.order_by('id').reverse()[0].id
                
            insert = GenereFilm(film_id=filmID, genere_id=genID)
            insert.save()     
            
        conferma= "Film correctly inserted"
    return scheda(request, filmID, conferma)  


#Update trailer
def upd_trailer(request):
    set_key(TMDB_KEY)
    
    film=Film.objects.filter(trailer='')
    
    for i in film:
        try:
            t=Movie(i.imdbId).youtube_trailers[0].source
            t = re.sub('&.*', '', t)                         

        except:
            t=''
        Film.objects.filter(imdbId=i.imdbId).update(trailer=t)
        
    alert='Trailers Updated'
    return render_to_response('alert.html', {'completed' : alert})
        
        
        
