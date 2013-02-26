from models import *
from mylib import *
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from datetime import datetime, date
from queries import *

def advice_genre(request):
    user = get_user(request)
    result = []

    query = 'SELECT distinct film_film.id, film_film.cover, film_film.titolo FROM auth_user, film_film, film_generefilm, film_genere, film_generepreferito WHERE film_film.id = film_generefilm.film_id AND film_genere.id = film_generefilm.genere_id AND film_generepreferito.genere_id = film_genere.id AND film_generepreferito.user_id = auth_user.id AND auth_user.id = %s AND film_film.id not in (SELECt film_id from film_preferito where utente_id = %s)'
    params = [user.id, user.id]
    result = db_query_params(request, query, params)
    
    for i in result:                          #elimina i doppioni
        if result.count(i) > 1:
           result.remove(i)

    return result


#stessa funzione di sopra ma tenendo conto del regista
def advice_reg(request):
    user = get_user(request)
    fav_user = Preferito.objects.filter(utente=user)
    resultrand= None
    result = []
    query = 'SELECT * FROM film_film WHERE id not in (SELECT film_id FROM film_preferito WHERE utente_id = %s)'
    all_film = db_query_params(request, query, user.id)

    if(len(fav_user) == 0):                                                             #se l'utente non ha inserito alcun film tra i preferiti
                     return None
    else:
         for p in all_film:                                           #per ciascun preferito
             counter = 0
             reg = Regia.objects.filter(film=p['id'])


             for f in fav_user:                                       #per ciascun film nella bd

                 regf= Regia.objects.filter(film=f.film)

                 for g in reg:
                     for gf in regf:
                         sfg = g.regista
                         shs = gf.regista
                         if(sfg == shs):
                              counter = counter +1           #incrementa di 1 il numero di corrispondenze
             if (counter >= 1):
                result.append(p)


    for i in result:                          #elimina i doppioni
        if result.count(i) > 1:
           result.remove(i)
           
    if(len(result) == 0):                                                             #se l'utente non ha inserito alcun film tra i preferiti
                     return None

    return result
    
    
#stessa funzione di sopra ma tenendo conto del regista
def advice_wri(request):
    user = get_user(request)
    fav_user = Preferito.objects.filter(utente=user)
    resultrand= None
    result = []
    query = 'SELECT * FROM film_film WHERE id not in (SELECT film_id FROM film_preferito WHERE utente_id = %s)'
    all_film = db_query_params(request, query, user.id)

    if(len(fav_user) == 0):                                                             #se l'utente non ha inserito alcun film tra i preferiti
        return None
    else:
        for p in all_film:                                           #per ciascun preferito
            counter = 0
            reg = Scrive.objects.filter(film=p['id'])

            for f in fav_user:                                       #per ciascun film nella bd
                regf= Scrive.objects.filter(film=f.film)
                for g in reg:
                    for gf in regf:
                        sfg = g.scrittore
                        shs = gf.scrittore
                        if(sfg == shs):
                            counter = counter +1           #incrementa di 1 il numero di corrispondenze
                if (counter >= 1):
                    result.append(p)


    for i in result:                          #elimina i doppioni
        if result.count(i) > 1:
            result.remove(i)
           
    if(len(result) == 0):                                                             #se l'utente non ha inserito alcun film tra i preferiti
        return None

    return result


#stessa funzione di sopra ma tenendo conto del regista
def advice_cast(request):
    user = get_user(request)

    result = []


    query = 'SELECT distinct film_film.id, film_film.cover, film_film.titolo FROM auth_user, film_film, film_filmcast, film_attore, film_attorepreferito WHERE film_film.id = film_filmcast.film_id AND film_attore.id = film_filmcast.attore_id AND film_attorepreferito.attore_id = film_attore.id AND film_attorepreferito.user_id = auth_user.id AND auth_user.id = %s AND film_film.id not in (SELECt film_id from film_preferito where utente_id = %s)'
    params = [user.id, user.id]
    result = db_query_params(request, query, params)
    for i in result:                          #elimina i doppioni
        if result.count(i) > 1:
            result.remove(i)
    return result


def advice_friend_profile(request):

    user = get_user(request)
    fav_user = Preferito.objects.filter(utente=user)
    resultrand = None
    result = []
    query = 'SELECT * FROM auth_user, film_profilo WHERE auth_user.id = film_profilo.user_id AND is_superuser = 0 AND auth_user.id <> %s'
    all_users = db_query_params(request, query, user.id)
    pu = None
    params = [user.id, user.id, user.id]                                                          #se l'utente non ha inserito alcun film tra i preferiti

    if(len(fav_user) == 0):
        return result

    else:
        for f in all_users:                                       #per ciascun film nella bd
            counter = 0
            favu = Preferito.objects.filter(utente=f['user_id'])
            perc = (len(favu)*50)/100
            percusr = (len(fav_user)*50)/100
            if(perc  != 0):
                for pu in fav_user:
                    for pusr in favu:
                        titolo1 = pusr.film
                        titolo = pu.film
                        if(titolo == titolo1):
                                counter = counter+1
                if((counter >= perc) or (counter >= percusr)):
                    presente = Amicizia.objects.filter(user=user, amico=f['user_id'])
                    presenteinv = Amicizia.objects.filter(user=f['user_id'], amico=user)
                    if (len(presente) == 0):
                        if (len(presenteinv) == 0):
                            result.append(f)

    for i in result:
        if result.count(i) > 1:
            result.remove(i)
           
    if(len(result) == 0):
        return result


    return result
    
    
    




def advice_friend_topic(request):

    user = get_user(request)
    topic_user = TopicCommento.objects.filter(user=user)

    resultrand = None
    result = []

    query = 'SELECT * FROM auth_user, film_profilo WHERE auth_user.id = film_profilo.user_id AND is_superuser = 0 AND auth_user.id <> %s'
    all_users = db_query_params(request, query, user.id)


    if(len(topic_user) == 0):
                     return None

    else:
         for f in all_users:                                       #per ciascun film nella bd
             counter = 0
             topu = TopicCommento.objects.filter(user=f['user_id'])
             perc = (len(topu)*50)/100
             percusr = (len(topic_user)*50)/100
             if(perc  != 0):
                      for t in topu:
                          for tu in topic_user:
                              topic1 = t.topic
                              topic2 = tu.topic
                              if(topic1 == topic2):
                                        counter = counter+1

                      if((counter >= perc) or (counter >= percusr)):
                                 presente = Amicizia.objects.filter(user=user, amico=f['user_id'])
                                 presenteinv = Amicizia.objects.filter(user=f['user_id'], amico=user)
                                 if (len(presente) == 0):
                                    if (len(presenteinv) == 0):
                                       result.append(f)

    for i in result:
        if result.count(i) > 1:
           result.remove(i)
           
    if(len(result) == 0):                                                             #se l'utente non ha inserito alcun film tra i preferiti
                     return None


    return result
    
    
    



def advice_friend_profile2(request):
    result = []
    user = get_user(request)
    profilo = Profilo.objects.get(user=user)
    
    query = 'SELECT * FROM auth_user , film_profilo WHERE auth_user.id = film_profilo.user_id AND user_id <> %s AND (DATEDIFF(film_profilo.eta,%s) >= -365 OR DATEDIFF(film_profilo.eta,%s) <= 365) AND (film_profilo.paese = %s OR film_profilo.citta = %s) group by rand() Limit 3'
    params = [user.id, profilo.eta,profilo.eta, profilo.paese, profilo.citta]
    results = db_query_params(request, query, params)


    return results
    



def adv_newgroups(request):
    user = get_user(request)
    query ='select distinct auth_group.name, auth_group.id from auth_group, film_profilogruppo, film_iscrizione, auth_user WHERE auth_group.id = film_profilogruppo.group_id AND film_iscrizione.group_id = auth_group.id AND film_iscrizione.user_id = auth_user.id AND auth_group.id not in (SELECT group_id from film_iscrizione WHERE user_id = %s) AND film_profilogruppo.user_id <> %s AND film_profilogruppo.date >= curdate() - 1  group by rand() limit 5'
    params = [user.id, user.id]
    result = db_query_params(request, query, params)

    return result
    
    
def adv_groups(request):
    user = get_user(request)


    query ='select distinct auth_group.name, auth_group.id from auth_group, film_profilogruppo, film_iscrizione, auth_user, film_amicizia WHERE auth_group.id = film_profilogruppo.group_id AND film_iscrizione.group_id = auth_group.id AND film_iscrizione.user_id = auth_user.id AND auth_group.id not in (SELECT group_id from film_iscrizione WHERE user_id = %s) AND film_profilogruppo.user_id <> %s AND ((film_amicizia.user_id = %s) OR (film_amicizia.amico_id = %s)) group by rand() limit 5'
    params = [user.id, user.id, user.id , user.id]
    result = db_query_params(request, query, params)

    return result

def adv_user_genre(request):
    user = request.session ['user_id']
    
    view= 'create or replace view generi_utente as select user_id, genere_id, descrizione FROM film_generepreferito as gp, film_genere as fg where user_id= %s and gp.genere_id=fg.id'
    params = [user]
    db_query_params(request, view, params)
    
    view= 'create or replace view lista_utenti as select gp.user_id from film_generepreferito gp, generi_utente gu where gp.genere_id=gu.genere_id and gp.user_id!=%s group by gp.user_id'
    params = [user]
    db_query_params(request, view, params)


    query='select u.id, u.username, p.name FROM auth_user as u, film_profilo as p, lista_utenti as lu where u.id=p.user_id and p.user_id=lu.user_id'
    params = []
    result = db_query_params(request, query, params)

    return result