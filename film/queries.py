from mylib import *
from myfunct import *

def get_hottopics(request):
    query = 'SELECT topic_id, descrizione, count( * ) as num FROM film_topic, film_topiccommento WHERE film_topic.id = film_topiccommento.topic_id GROUP BY film_topic.id having count(*) >= 10 Order by count(*) DESC LIMIT 10'
    result = db_query(request, query)
    return result
    

def get_partecipazioni(request):
    user = get_user(request)
    partecipazioni = 'SELECT * FROM auth_group, auth_user, film_iscrizione, film_topic WHERE auth_group.id = film_iscrizione.group_id AND auth_user.id = film_iscrizione.user_id AND film_iscrizione.group_id = film_topic.group_id AND film_topic.date >= curdate() - 1 group by rand() limit 5'
    result = db_query(request, partecipazioni)
    return result

def get_iscrizioni(request):
    user = get_user(request)
    iscrizioni = 'SELECT * FROM auth_group, film_iscrizione WHERE auth_group.id = film_iscrizione.group_id AND film_iscrizione.user_id = %s ORDER BY auth_group.name'
    result = db_query_params(request, iscrizioni, user.id)
    return result
    
    
def get_profilo(request):
    user = get_user(request)
    result = Profilo.objects.get(user=user)
    return result
    

def get_notify(request):
    user = get_user(request)
    query = 'select * from auth_group,film_topic,film_topiccommento,auth_user where auth_group.id = film_topic.group_id AND auth_user.id = film_topiccommento.user_id AND film_topic.id = film_topiccommento.topic_id AND film_topiccommento.date >= curdate() - 1 AND film_topiccommento.user_id <> %s AND group_id in (select auth_group.id from auth_group, film_iscrizione, auth_user where film_iscrizione.user_id = auth_user.id AND film_iscrizione.group_id = auth_group.id AND film_iscrizione.user_id = %s) AND film_topic.id in (SELECT film_topic.id from film_topic, film_topiccommento where film_topiccommento.topic_id = film_topic.id AND film_topiccommento.user_id = %s) order BY film_topiccommento.date DESC'
    params = [user.id, user.id, user.id]
    result = db_query_params(request, query, params)
    return result
    
def get_mostvoted(request):
    query = 'select * from film_film where  film_film.id in (select film_id from film_voto group by film_id having count(*) in (select count(*)  from film_voto group by film_id  having count(*)  >=  ALL (select count(*)  from film_voto group by film_id))) limit 1'
    result = db_query(request, query)
    return result
    
def get_mostcomm(request):
    query = 'select * from film_film where  film_film.id in (select film_id from film_commento group by film_id having count(*) in (select count(*)  from film_commento group by film_id  having count(*)  >=  ALL (select count(*)  from film_commento group by film_id))) limit 1'
    result = db_query(request, query)
    return result
    
    
def get_lastadded(request):
    #query = 'select * from film_film where date >= curdate() - 1  group by rand() limit 10'
    query = 'SELECT * FROM film_film ORDER BY id DESC LIMIT 10'      #SELECT LAST 10 ADDED FILMS
    result = db_query(request, query)
    return result

def get_eventi(request):
    user = get_user(request)
    query = 'select film_commento.utente_id, film_commento.date, auth_user.username, film_film.id, titolo from film_commento, film_film, auth_user where film_commento.film_id = film_film.id AND auth_user.id = film_commento.utente_id and film_commento.date >= curdate() - 1 AND film_commento.utente_id <> %s AND film_commento.film_id in (select film_id from film_film, film_commento where film_commento.film_id = film_film.id AND utente_id = %s) order by film_commento.date DESC LIMIT 5'
    params = [user.id, user.id]
    result = db_query_params(request, query, params)
    return result
    
def get_friends(request, id=None):
    risultati = []
    
    if(id==None):
        user = get_user(request)
        userid = user.id
    else:
        userid = id

    amicidx = Amicizia.objects.filter(confermata=1, user=userid).values('amico')       #scorre la lista delle amicizie (lato dx)
    for i in amicidx:
        uamico = Profilo.objects.get(user_id=i['amico'])
        risultati.append(uamico)
        
    amicisx = Amicizia.objects.filter(confermata=1, amico=userid).values('user')       #scorre la lista delle amicizie (lato sx)
    for i in amicisx:
        uamico = Profilo.objects.get(user_id=i['user'])
        risultati.append(uamico)

    
    return risultati
    
    
    
def get_user_friends(request, id):

    risultati = []
    userid = id

    amicidx = Amicizia.objects.filter(confermata=1, user=userid).values('amico')       #scorre la lista delle amicizie (lato dx)
    for i in amicidx:
        uamico = Profilo.objects.get(user_id=i['amico'])
        risultati.append(uamico)
        
    amicisx = Amicizia.objects.filter(confermata=1, amico=userid).values('user')       #scorre la lista delle amicizie (lato sx)
    for i in amicisx:
        uamico = Profilo.objects.get(user_id=i['user'])
        risultati.append(uamico)

    
    return risultati

#following

def get_following(request, id):
    risultati = []
    query = 'select * from film_follower where user_id = %s'
    f = db_query_params(request, query, id)
    for i in f:
        u = User.objects.get(id=i['followed_id'])
        risultati.append(u)
    return risultati


def get_mostfollowed(request):
    result = []
    query = 'select distinct username, auth_user.id, film_profilo.name,  count(*) as num  from auth_user inner join film_follower on auth_user.id = film_follower.followed_id inner join film_profilo on film_profilo.user_id = auth_user.id group by followed_id order by count(*) DESC LIMIT 10'
    result = db_query(request, query)
    return result


def get_followed(request, id):
    risultati = []
    query = 'select user_id from film_follower where followed_id = %s'
    f = db_query_params(request, query, id)
    for i in f:
        u = User.objects.get(id=i['user_id'])
        risultati.append(u)
        

    return risultati

def get_filmID(request, imdbID):
    query = 'SELECT id FROM film_film WHERE imdbId= %s'
    filmID = db_query_params(request, query, imdbID)
    filmID=filmID[0]['id']
    return filmID