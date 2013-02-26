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
import re


#homepage
@login_required(login_url='/accounts/login/')
def ricerca(request):
    user = get_user(request)

    notify = get_notify(request)
    notify = pagination(request,notify, 5)
    mostvoted = get_mostvoted(request)
    mostcomm = get_mostcomm(request)
    lastadded = get_lastadded(request)
    eventi = get_eventi(request)

    nfollow = Follower.objects.filter(followed = user).count()

    nome = user.username

    eventi = pagination(request,eventi, 5)
    lastadded = pagination(request,lastadded, 10)

    richieste = Amicizia.objects.filter(amico = user.id, confermata = False)           #cerca se ci sono richieste di amicizia non confermate

    return render_to_response('main.html', {'nfollow' : nfollow, 'notify' : notify , 'eventi' : eventi , 'username' : nome, 'lastadded' : lastadded, 'richieste' : richieste, 'mostcomm' : mostcomm, 'mostvoted' : mostvoted})
   



#accesso a IMDb
@login_required(login_url='/accounts/login/')
def imdb(request, id):

    risultati =  None
    ia = IMDb()
    risultati = ia.get_movie(id)

    return render_to_response('imdb/scheda.html', {
    'risultati': risultati})

    
#inserimento film
@login_required(login_url='/accounts/login/')
def insert_film(request, id):
    conferma = "Film already existing"
    presente = None
    ia = IMDb()
    risultati = ia.get_movie(id)
    presente = Film.objects.filter(imdbId__iexact=id)
    if(len(presente) == 0):
                     for i in risultati['distributor']:                       #attori
                         dato= i['name']
                         presente = Compagnia.objects.filter(descrizione__iexact=dato)
                         if(len(presente) == 0):
                                          company = Compagnia(descrizione=i['name'])
                                          company.save()
                     for i in risultati['cast']:                       #attori
                         dato= i['name']
                         presente = Attore.objects.filter(nome__iexact=dato)
                         if(len(presente) == 0):
                                          actor = Attore(nome=i['name'])
                                          actor.save()
                     for i in risultati['cast']:                       #personaggi
                         dato= i.currentRole
                         if(len(dato) == 1):
                                      datoid = dato["name"]
                                      presente = Personaggio.objects.filter(descrizione__iexact=datoid)
                                      if(len(presente) == 0):
                                                           charact = Personaggio(descrizione=datoid)
                                                           charact.save()
                         else:
                                      if(len(dato) > 1):
                                                   for j in dato:
                                                       datoid = j["name"]
                                                       presente = Personaggio.objects.filter(descrizione__iexact=datoid)
                                                       if(len(presente) == 0):
                                                                        charact = Personaggio(descrizione=datoid)
                                                                        charact.save()

                     for i in risultati['director']:                   #registi
                         dato= i['name']
                         presente = Regista.objects.filter(nome__iexact=dato)
                         if(len(presente) == 0):
                                          direct = Regista(nome=i['name'])
                                          direct.save()
                     for i in risultati['writer']:                     #scrittori
                         dato= i['name']
                         presente = Scrittore.objects.filter(nome__iexact=dato)
                         if(len(presente) == 0):
                                          writ = Scrittore(nome=i['name'])
                                          writ.save()
                     for i in risultati['genre']:                      #generi
                         dato= i
                         presente = Genere.objects.filter(descrizione__iexact=dato)
                         if(len(presente) == 0):
                                          genere = Genere(descrizione=i)
                                          genere.save()
                     for i in risultati['country']:                    #paesi
                         dato= i
                         presente = Paese.objects.filter(descrizione__iexact=dato)
                         if(len(presente) == 0):
                                          country = Paese(descrizione=i)
                                          country.save()
                     for i in risultati['language']:                   #lingue
                         dato= i
                         presente = Lingua.objects.filter(descrizione__iexact=dato)
                         if(len(presente) == 0):
                                          lang = Lingua(descrizione=i)
                                          lang.save()
                     tr = risultati['plot'].pop()                      #trama
                     tit = risultati['title']                          #titolo
                     try:
                         cover = re.sub(r'\._V1\._SX(\d+)_SY(\d+)_', '', risultati['cover'])                         
                     except:
                            cover = None
                     year = risultati['year']
                     film = Film(titolo=tit, trama = tr, cover = cover, imdbId = id, anno = year)  #film
                     film.save()

                     for i in risultati['cast']:   #inserimento cast
                         a = i['name']
                         t = risultati['title']

                         id1 = Film.objects.get(titolo__iexact=t).id
                         id2 = Attore.objects.get(nome__iexact=a).id
                         presente = Filmcast.objects.filter(film=id1, attore=id2)
                         if(len(presente) == 0):
                                          inserimento = Filmcast(film_id=id1, attore_id=id2)
                                          inserimento.save()

                     for i in risultati['distributor']:   #inserimento distributori
                         a = i['name']
                         t = risultati['title']

                         id1 = Film.objects.get(titolo__iexact=t).id
                         id2 = Compagnia.objects.get(descrizione__iexact=a).id
                         presente = CompagniaFilm.objects.filter(film=id1, compagnia=id2)
                         if(len(presente) == 0):
                                          inserimento = CompagniaFilm(film_id=id1, compagnia_id=id2)
                                          inserimento.save()

                     for i in risultati['genre']:   #inserimento genere
                         t = risultati['title']

                         id1 = Film.objects.get(titolo__iexact=t).id
                         id2 = Genere.objects.get(descrizione__iexact=i).id
                         presente = GenereFilm.objects.filter(film=id1, genere=id2)
                         if(len(presente) == 0):
                                          inserimento = GenereFilm(film_id=id1, genere_id=id2)
                                          inserimento.save()

                     for i in risultati['country']:   #inserimento paese
                         t = risultati['title']

                         id1 = Film.objects.get(titolo__iexact=t).id
                         id2 = Paese.objects.get(descrizione__iexact=i).id
                         presente = Set.objects.filter(film=id1, paese=id2)
                         if(len(presente) == 0):
                                          inserimento = Set(film_id=id1, paese_id=id2)
                                          inserimento.save()

                     for i in risultati['language']:   #inserimento genere
                         t = risultati['title']

                         id1 = Film.objects.get(titolo__iexact=t).id
                         id2 = Lingua.objects.get(descrizione__iexact=i).id
                         presente = LinguaFilm.objects.filter(film=id1, lingua=id2)
                         if(len(presente) == 0):
                                          inserimento = LinguaFilm(film_id=id1, lingua_id=id2)
                                          inserimento.save()

                     for i in risultati['director']:   #inserimento regia
                         t = risultati['title']
                         d = i['name']
                         id1 = Film.objects.get(titolo__iexact=t).id
                         id2 = Regista.objects.get(nome__iexact=d).id
                         presente = Regia.objects.filter(film=id1, regista=id2)
                         if(len(presente) == 0):
                                          inserimento = Regia(film_id=id1, regista_id=id2)
                                          inserimento.save()

                     for i in risultati['writer']:   #inserimento scrittore
                         t = risultati['title']
                         w = i['name']
                         id1 = Film.objects.get(titolo__iexact=t).id
                         id2 = Scrittore.objects.get(nome__iexact=w).id
                         presente = Scrive.objects.filter(film=id1, scrittore=id2)
                         if(len(presente) == 0):
                                          inserimento = Scrive(film_id=id1, scrittore_id=id2)
                                          inserimento.save()

                     for i in risultati['cast']:   #inserimento cast
                         act = i['name']
                         a = i.currentRole
                         if(len(a) == 1):
                                   c = a['name']
                                   t = risultati['title']

                                   id1 = Film.objects.get(titolo__iexact=t).id
                                   id2 = Personaggio.objects.get(descrizione__iexact=c).id
                                   actor = Attore.objects.get(nome__iexact=act).id
                                   presente = Compare.objects.filter(film=id1, personaggio=id2)
                                   if(len(presente) == 0):
                                                           inserimento = Compare(film_id=id1, personaggio_id=id2, attore_id=actor)
                                                           inserimento.save()
                                                           conferma = "Film correctly inserted"

                         else:
                              if(len(a) > 1):
                                        for j in a:
                                            c = j['name']
                                            t = risultati['title']
                                            id1 = Film.objects.get(titolo__iexact=t).id
                                            id2 = Personaggio.objects.get(descrizione__iexact=c).id
                                            actor = Attore.objects.get(nome__iexact=act).id
                                            presente = Compare.objects.filter(film=id1, personaggio=id2)
                                            if(len(presente) == 0):
                                                             inserimento = Compare(film_id=id1, personaggio_id=id2, attore_id=actor)
                                                             inserimento.save()
                                                             conferma = "Film correctly inserted"
                     return render_to_response('alert.html', {'completed' : conferma})
    else:
         return render_to_response('alert.html', {'completed' : conferma})






