from models import *
import MySQLdb
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from settings import *
from mylib import *
from myfunct import *
from queries import *
from classes import *



#ricerca film in imdb
@login_required(login_url='/accounts/login/')
def insGruppo(request):

    userid = get_user(request)
    groupid = None
    presente = None
    completed = None
    username = None
    present = None
    username = userid.username
    
    newgroups = adv_newgroups(request)
    adv_group = adv_groups(request)

    if request.method == 'POST':
       form = creaGruppo(request.POST)
       if form.is_valid():
          groupname = form.cleaned_data['nome']
          descr = form.cleaned_data['desc']
          import textwrap
          descr = textwrap.fill(descr)
          presente = Group.objects.filter(name=groupname)
          if (len(presente) == 0):
             group = Group.objects.create(name=groupname)
             group.save()
             groupid = Group.objects.get(name = groupname)
             inserimento = ProfiloGruppo(user=userid, group=groupid, descrizione = descr)
             inserimento.save()
             inserimento = Iscrizione(user=userid, group = groupid)
             inserimento.save()
             completed = "Completed"
          else:
                present = "This group is already present..."
                form = creaGruppo()
    else:
         form = creaGruppo()
    return render_to_response('groups/group.html', {
                                                    'user': request.session['user'],
                                                    'img_prof': request.session['img_prof'], 
                                                    'adv_group' : adv_group, 
                                                    'newgroups' : newgroups, 
                                                    'form': form, 
                                                    'completed' : completed, 
                                                    'present' : present, 
                                                    'username' : username, 
                                                    'groupid' : groupid, 
                                                    'userid' : userid
                                                    })
    

@login_required(login_url='/accounts/login/')
def selectGruppo(request):
    query = None
    posts = None
    form = ricercaGruppo(request.POST)
    nogroup = None


    user = get_user(request)
    hotopics = get_hottopics(request)
    query_part = get_partecipazioni(request)
    adv_usr = advice_friend_topic(request)
    query_iscr = get_iscrizioni(request)
    


    if form.is_valid():
       g = form.cleaned_data['gruppo']
       query = Group.objects.filter(name__icontains=g)
       if(len(query) == 0):
                     nogroup = "No match found"
                     return render_to_response('alert.html', {'completed' : nogroup})


       posts = pagination(request, query, 10)
    else:
         form = ricercaGruppo()
    return render_to_response('groups/groupSearch.html', {
    'form': form, 'adv_usr' : adv_usr, 'posts': posts,  'query_part' : query_part,'query_iscr' : query_iscr, 'user' : user,'hotopics' : hotopics})


@login_required(login_url='/accounts/login/')
def subscribe(request, id):

    iscrizione = None
    notopic = None
    notmember = None
    form = formTopic(request.POST)
    userid = get_user(request)
    group = Group.objects.get(id=id)
    profilo = ProfiloGruppo.objects.get(group=id) 

    numuser = Iscrizione.objects.filter(group=id).count()
    if(numuser == 0):
               numuser=1

    presente = Iscrizione.objects.filter(user=userid.id, group=id)
    if (len(presente) == 0):
       inserimento = Iscrizione(user=userid, group=group)
       inserimento.save()
       iscrizione = "Subscribe completed"
       notmember = 1


    topics = Topic.objects.filter(group=group)
    posts = pagination(request, topics, 10)
    if (len(topics) == 0):
       notopic  = "No topic inserted"

    return render_to_response('groups/topics.html', {'numuser' : numuser,
    'posts': posts, 'form': form, 'iscrizione': iscrizione, 'group' : group, 'notopic' : notopic, 'user' : userid, 'desc' : profilo})


@login_required(login_url='/accounts/login/')
def topics(request,id):
    iscr = None
    notmember =None
    notopic = None
    numuser = None

    form = formTopic(request.POST)
    group = Group.objects.get(id=id)   
    desc = ProfiloGruppo.objects.get(group=id)                           #gruppo
    profilo = ProfiloGruppo.objects.get(group=id).user                   #profilo del gruppoo
    userid = get_user(request)                                           #utente loggato
    presente = Iscrizione.objects.filter(user=userid.id, group=id)       #se l'utente loggato non e membro del gruppo
    boss = Group.objects.filter(id=id, user = userid)
    
    presente2 = Iscrizione.objects.filter(user=userid.id, group=id).exclude(user = userid)
    if (len(presente) == 0):
        notmember = 1

    if (len(presente) != 0):
        iscr= 1


    numuser = Iscrizione.objects.filter(group=id).count()
    if(numuser == 0):
               numuser=1



    topics = Topic.objects.filter(group=group)                           #trova i topics del gruppo
    posts = pagination(request, topics, 10)
    if (len(topics) == 0):
       notopic  = "No topic inserted"

    return render_to_response('groups/topics.html', {
                                                     'user': request.session['user'],
                                                     'img_prof': request.session['img_prof'], 
                                                     'posts': posts, 
                                                     'iscr' : iscr, 
                                                     'form': form, 
                                                     'group' : group, 
                                                     'notopic' : notopic, 
                                                     'profilo' : profilo, 
                                                     'notmember' : notmember, 
                                                     'numuser' : numuser, 
                                                     'desc' : desc
                                                     })





@login_required(login_url='/accounts/login/')
def instopic(request, id):
    notopic =None
    presente=None
    topicadded = None
    userid = get_user(request)
    group = Group.objects.get(id=id)
    form = formTopic(request.POST)

    desc = ProfiloGruppo.objects.get(group=id)
    presente = Iscrizione.objects.filter(user=userid.id, group=id)       #se l'utente loggato non e membro del gruppo
    boss = Group.objects.filter(id=id, user = userid)

    if (len(presente) == 0):
       notopic = "You should join this group first!!!"
       form = formTopic()

    if form.is_valid():
       t = form.cleaned_data['topic']
       presente = Topic.objects.filter(descrizione=t)
       if (len(presente)==0):
          inserimento = Topic(user=userid, group=group, descrizione=t)
          inserimento.save()
          commento = form.cleaned_data['commento']
          import textwrap
          commento = textwrap.fill(commento)
          top = Topic.objects.get(descrizione=t, group=group)
          inserimento = TopicCommento(topic_id=top.id, user=userid, commento=commento)
          inserimento.save()                  
          topicadded = "Topic added succesfully"
       else:
            form = formTopic()

    else:
         form = formTopic()

    topics = Topic.objects.filter(group=group)
    posts = pagination(request, topics, 10)
    if (len(topics) == 0):
       notopic  = "No topic inserted"

    return render_to_response('groups/topics.html', {
                                                     'user': request.session['user'],
                                                     'img_prof': request.session['img_prof'], 
                                                     'posts': posts, 
                                                     'group' : group, 
                                                     'form': form, 
                                                     'notopic' : notopic, 
                                                     'topicadded' :topicadded, 
                                                     'user' : userid, 
                                                     'desc' : desc})
    


@login_required(login_url='/accounts/login/')
def showTopic(request,id):

    notmember = None
    form = None
    presente = None
    accesso = None
    commentato = None                                          #inizializzazione
    risultati = None
    username = None
    boss = None
    user = get_user(request)
    topics = Topic.objects.get(id=id)
    g =  Topic.objects.filter(id=id).values('group_id')
    name = topics.descrizione
    presente = Iscrizione.objects.filter(user=user, group=topics.group)
    
    
    


    
    query = 'select * from auth_group, film_topic where auth_group.id = film_topic.group_id AND film_topic.id = %s'
    group = db_query_params(request, query,id)
    for i in g:
        boss = Group.objects.get(id = i['group_id'])


    if((len(presente) != 0)):
                     accesso = 1  
                     query = 'select film_topiccommento.id as commento_id, auth_user.id, film_profilo.name, auth_user.username, film_topiccommento.date, film_topiccommento.commento from film_topiccommento, film_profilo, auth_user where auth_user.id = film_profilo.user_id AND film_profilo.user_id = film_topiccommento.user_id AND topic_id = %s ORDER by film_topiccommento.date DESC'
                     risultati = db_query_params(request, query, id)
                     posts = pagination(request, risultati, 5)
                     form = formTopicComm(request.POST)
                     if form.is_valid():
                        idutente = get_user(request)
                        commento = form.cleaned_data['commento']
                        import textwrap
                        commento = textwrap.fill(commento)
                        inserimento = TopicCommento(topic_id=id, user_id=user.id, commento=commento)
                        inserimento.save() 

                        tc = TopicCommento.objects.get(commento = commento)
                        query = 'select distinct user_id from auth_user, film_topiccommento where auth_user.id = film_topiccommento.user_id AND topic_id = %s AND auth_user.id <> %s'
                        params = [id, user.id]
                        partecipanti = db_query_params(request, query, params)



                        form = formTopicComm()
                        commentato = 1

                     else:
                          form = formTopicComm()
                     return render_to_response('groups/topic.html', {
                                                                     'user': request.session['user'],
                                                                     'img_prof': request.session['img_prof'], 
                                                                     'accesso': accesso, 
                                                                     'name' : name, 
                                                                     'topic' : id, 
                                                                     'posts': posts, 
                                                                     'username' : user.username, 
                                                                     'form' : form, 
                                                                     'commentato' : commentato
                                                                     })


    else:
         notmember = "You should subscribe first too see topics"
         return render_to_response('alert.html', {
                                                  'user': request.session['user'],
                                                  'img_prof': request.session['img_prof'], 
                                                  'completed' : notmember
                                                  })




@login_required(login_url='/accounts/login/')
def reportTopic(request, id):

    conferma = None

    a = TopicCommento.objects.filter(id=id).update(reported=True)             #conferma l'amicizia
    conferma = "You have reported this comment"
    return render_to_response('alert.html', {
                                             'user': request.session['user'],
                                             'img_prof': request.session['img_prof'], 
                                             'completed' : conferma
                                             })


