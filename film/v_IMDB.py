from django.shortcuts import render_to_response
import urllib
import json
from classes import *
from models import *
from django.contrib.auth.decorators import login_required
import re
from views_film import scheda
from queries import get_filmID

#Ricerca in IMDB tramite omdbapi.com
def search_IMDB (titolo):
    sito='http://www.omdbapi.com/?s='+titolo
    
    r=0
    r=json.loads(urllib.urlopen(sito).read())
    
    i=0
    filmList = []
    try:
        for i in r['Search']:
            filmList.append(ricerca_IMDB(i['Title'], i['Year'], i['imdbID']))
    except:
        filmList = []
    
    return filmList



#Inserimento Film richiesto nel DB
def insert_IMDB (request, imdbID):
    sito='http://www.omdbapi.com/?i='+imdbID+'&plot=full'
    
    r=0
    r=json.loads(urllib.urlopen(sito).read())
    
    presente=0
    presente = Film.objects.filter(imdbId__iexact=imdbID)
    conferma= "Film already existing"
    
    if(len(presente) != 0): 
        filmID=get_filmID(request, imdbID)
        
    if(len(presente) == 0):       
        title = r['Title']
        plot = r['Plot']
        year = r['Year']
        cover = '/static/img/nocover.png'
        if (r['Poster'] != 'N/A'):
            cover = r['Poster']
        try:
            cover = re.sub(r'\._V1\._SX(\d+)_SY(\d+)_', '', cover)                         
        except:
            cover = None
        
        film = Film(titolo = title, trama = plot, cover = cover, imdbId = imdbID, anno = year)  #film
        film.save()
        filmID = Film.objects.order_by('id').reverse()[0].id
        
        #Splitto le stringhe multiple e le inserisco nel DB
        actors = []
        actors.append(r['Actors'].rstrip().split(', '))
        i=0
        for i in actors[0]:
            pres = Attore.objects.filter(nome__iexact=i)
            if(len(pres) > 0):
                actID = Attore.objects.get(nome__iexact=i).id
                
            if(len(pres) == 0):
                insert = Attore(nome=i)
                insert.save()
                actID = Attore.objects.order_by('id').reverse()[0].id
            
            insert=0    
            insert = Filmcast(film_id=filmID, attore_id=actID)
            insert.save()        
                
        director = []
        director.append(r['Director'].rstrip().split(', '))
        for i in director[0]:
            pres = Regista.objects.filter(nome__iexact=i)
            if(len(pres) > 0):
                dirID = Regista.objects.get(nome__iexact=i).id    
            
            if(len(pres) == 0):
                insert = Regista(nome=i)
                insert.save()      
                dirID = Regista.objects.order_by('id').reverse()[0].id
                
            insert = Regia(film_id=filmID, regista_id=dirID)
            insert.save()       
                     
        genre = []
        genre.append(r['Genre'].rstrip().split(', '))
        for i in genre[0]:            
            pres = Genere.objects.filter(descrizione__iexact=i)
            if(len(pres) > 0):
                genID = Genere.objects.get(descrizione__iexact=i).id
                
            if(len(pres) == 0):
                insert = Genere(descrizione=i)
                insert.save()
                genID = Genere.objects.order_by('id').reverse()[0].id
                
            insert = GenereFilm(film_id=filmID, genere_id=genID)
            insert.save()
                
        writer = []
        writer.append(r['Writer'].rstrip().split(', '))
        for i in writer[0]:
            pres = Scrittore.objects.filter(nome__iexact=i)
            if(len(pres) > 0):
                wriID = Scrittore.objects.get(nome__iexact=i).id
            
            if(len(pres) == 0):
                insert = Scrittore(nome=i)
                insert.save()
                wriID = Scrittore.objects.order_by('id').reverse()[0].id
                
            insert = Scrive(film_id=filmID, scrittore_id=wriID)
            insert.save()        
        
            conferma= "Film correctly inserted"
        
        
    #return render_to_response('alert.html', {'completed' : conferma})
    return scheda(request, filmID, conferma)

def test(request):

    pres= get_filmID(request, 'tt0466909')
    
    
    return render_to_response('test.html', {'id' : pres})
        
    
