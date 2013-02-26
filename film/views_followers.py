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
from views_users import profilo


@login_required(login_url='/accounts/login/')
def follow(request, id):

    alert = None
    user = get_user(request)
    alreadyFollow = Follower.objects.filter(user=user.id, followed=id)

    if (len(alreadyFollow) != 0):                                                                    #se i due utenti sono gia amici
        alert = "Already followed"
        #return render_to_response('alert.html', {'completed' : conferma})
        return profilo(request, id, alert)
    
    inserimento = Follower(user_id=user.id, followed_id=id)
    inserimento.save()
    alert = "Now you are following this user"                                            #altrimenti manda opportuno messaggio di errore
    #return render_to_response('alert.html', {'completed' : conferma})
    return profilo(request, id, alert)


@login_required(login_url='/accounts/login/')
def allFollow(request , id=None, alert=None):

    risultati = []
    user = id
    query = 'select * from film_follower where user_id = %s'
    f = db_query_params(request, query, id)
    

    if(len(f) == 0):
        notfriends = "You haven't added any users to follow yet"
        return render_to_response('alert.html', {'user': request.session['user'], 'img_prof': request.session['img_prof'], 'completed' : notfriends})

    for i in f:
        u = Profilo.objects.get(user_id=i['followed_id'])
        risultati.append(u)
        
    follow = pagination(request, risultati, 20)
    
    user = User.objects.get(id=id)
    
    #altrimenti manda opportuno messaggio di errore
    return render_to_response('users/all_details.html', {
                                                         'user': request.session['user'],
                                                         'img_prof': request.session['img_prof'], 
                                                         'follow' : follow,
                                                         'rel': user,
                                                         'alert': alert
                                                         })
    
@login_required(login_url='/accounts/login/')
def allFollower(request , id=None):

    risultati = []
    user = id
    query = 'select * from film_follower where followed_id = %s'
    f = db_query_params(request, query, id)
    

    if(len(f) == 0):
        notfriends = "You haven't any follower yet"
        return render_to_response('alert.html', {'user': request.session['user'], 'img_prof': request.session['img_prof'], 'completed' : notfriends})

    for i in f:
        u = Profilo.objects.get(user_id=i['user_id'])
        risultati.append(u)
        
    follower = pagination(request, risultati, 50)

    #altrimenti manda opportuno messaggio di errore
    return render_to_response('users/all_details.html', {
                                                         'user': request.session['user'],
                                                         'img_prof': request.session['img_prof'], 
                                                         'follower' : follower
                                                         })    
 
 
@login_required(login_url='/accounts/login/')
def actions(request, id):

    user = get_user(request)
    profilo = Profilo.objects.get(user=id)
    noactivity = None


    iscrizioni = 'SELECT * FROM auth_group, film_iscrizione WHERE auth_group.id = film_iscrizione.group_id AND film_iscrizione.user_id = %s ORDER BY auth_group.name'
    iscr = db_query_params(request, iscrizioni, id)
    iscrizioni = pagination(request, iscr, 10)
  
    query = 'select film_commento.date, auth_user.username, film_film.id, titolo from film_commento, film_film, auth_user where film_commento.film_id = film_film.id AND auth_user.id = film_commento.utente_id and film_commento.date >= curdate() - 2 AND film_commento.utente_id = %s order by film_commento.date DESC LIMIT 5'
    comm = db_query_params(request, query, id)
    comments = pagination(request, comm, 10)

    query = 'select * from auth_group,film_topic,film_topiccommento,auth_user where auth_group.id = film_topic.group_id AND auth_user.id = film_topiccommento.user_id AND film_topic.id = film_topiccommento.topic_id  AND film_topiccommento.user_id = %s order BY film_topiccommento.date DESC'
    top = db_query_params(request, query, id)
    topics = pagination(request, top, 10)

    query = 'SELECT * FROM film_film INNER JOIN film_preferito ON film_film.id = film_preferito.film_id where utente_id = %s'
    f_u = db_query_params(request, query, id)
    posts = pagination(request, f_u, 10)

    if(len(iscr) == 0 and len(comm) == 0 and len(top) == 0 and len(f_u) == 0):
        noactivity = "No activity"
        return render_to_response('alert.html', {'completed' : noactivity})


    return render_to_response('users/profileFollower.html', {'user' : user , 'comments' : comments, 'iscrizioni' : iscrizioni , 'topics' : topics, 'posts' : posts, 'profilo' : profilo})



