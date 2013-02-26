import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from mylib import *
from myfunct import *
from classes import *
from views_imdb import *
from random import choice
import random





def testUsers(request):
    completed = None
    try:

        lista = []
        onetoten = range(1,121)
        gender = None
        hometown = None
        count = 0
        for count in onetoten:

            userid = "user" + str(count)
            count = count + 1
            password = 'silvia'
            email = userid + "@live.it"
            nome = get_random_word(request, 4)
            cognome = get_random_word(request, 4)


            c = ['Italy', 'United States of America', 'United Kingdom', 'France', 'Germany', 'Russia', 'Spain', 'Peru', 'Japan', 'China', 'India', 'Brasil']
            country = choice(c)

            if country == 'Italy':
               home = ['Milano', 'Roma', 'Napoli', 'Venezia', 'Bologna', 'Firenze', 'Genova', 'Perugia']
               hometown = choice(home)

            if country == 'Brasil':
               home = ['San Paulo', 'Rio de Janeiro']
               hometown = choice(home)

            if country == 'United States of America':
               home = ['New York', 'Los Angeles', 'Washington', 'Lancaster', 'Miami', 'Niagara Falls', 'Philadelphia', 'Seattle']
               hometown = choice(home)

            if country == 'India':
               home = ['Bombay', 'Delhi']
               hometown = choice(home)

            if country == 'United Kingdom':
               home = ['London', 'Liverpool', 'Oxford', 'Cambridge']
               hometown = choice(home)

            if country == 'France':
               home = ['Paris', 'Lion', 'Marseille']
               hometown = choice(home)

            if country == 'Spain':
               home = ['Madrid', 'Barcellona', 'Valencia', 'Granada']
               hometown = choice(home)

            if country == 'Germany':
               home = ['Berlin', 'Baden Baden', 'Amburg', 'Dussendorf', 'Frankfurt']
               hometown = choice(home)

            if country == 'Russia':
               home = ['Moscow', 'San Petersburg']
               hometown = choice(home)

            if country == 'Peru':
               home = ['Lima', 'Talara']
               hometown = choice(home)

            if country == 'Japan':
               home = ['Tokio', 'Fukushima']
               hometown = choice(home)

            if country == 'China':
               home = ['Beijing', 'Shangai']
               hometown = choice(home)

            g = ['m', 'f']
            gender = choice(g)


            d1 = datetime.strptime('1/1/1960 1:30 PM', '%m/%d/%Y %I:%M %p')
            d2 = datetime.strptime('1/1/1995 4:50 AM', '%m/%d/%Y %I:%M %p')
            date = random_date(d1, d2)

            user = User.objects.create_user(username=userid, email=email, password=password)     #inserimento dati
            user.is_staff = True
            user.save()
            userid = User.objects.get(username = userid).id
            inserimento = Profilo(user=user, nome=nome, cognome=cognome, paese=country, citta=hometown, eta=date, gender=gender)
            inserimento.save()
            completed = "Test completed"

    except:

           completed = "Test failed"
    return render_to_response('admin/alert.html', {'completed' : completed})




def testFav(request):
    completed = None

    try:

        nfilml =[]

        users = User.objects.exclude(is_superuser=1)




        query = 'SELECT max(id) as mid FROM film_attore'
        nusers = db_query(request, query)
        for i in nusers:
            a = int(i['mid'])
        query = 'SELECT max(id) as mid FROM film_genere'
        nusers = db_query(request, query)
        for i in nusers:
            g = int(i['mid'])
        query = 'SELECT max(id) as mid FROM film_regista'
        nusers = db_query(request, query)
        for i in nusers:
            r = int(i['mid'])



        for u in users:
            npre = random.randint(1, 10)
            npref = range(1,npre)
            for p in npref:

                query = 'SELECT id FROM film_film group by rand() limit 1'
                nfilm = db_query(request, query)

                for i in nfilm:
                    val= int(i['id'])

                

                valact = random.randint(1, a)
                valgen = random.randint(1, g)
                valreg = random.randint(1, r)

                film = Film.objects.get(id = val)
                presente = Preferito.objects.filter(utente=u, film=film)
                if(len(presente) == 0):
                                 inserimento = Preferito(utente=u, film=film)
                                 inserimento.save()

                act = Attore.objects.get(id = valact)
                presente = AttorePreferito.objects.filter(user=u, attore=act)
                if(len(presente) == 0):
                                 inserimento = AttorePreferito(user=u, attore=act)
                                 inserimento.save()

                gen = Genere.objects.get(id = valgen)
                presente = GenerePreferito.objects.filter(user=u, genere=gen)
                if(len(presente) == 0):
                                 inserimento = GenerePreferito(user=u, genere=gen)
                                 inserimento.save()

                reg = Regista.objects.get(id = valreg)
                presente = RegistaPreferito.objects.filter(user=u, regista=reg)
                if(len(presente) == 0):
                                 inserimento = RegistaPreferito(user=u, regista=reg)
                                 inserimento.save()


        completed = "Test completed"
    except:
           completed = "Test failed"

    return render_to_response('admin/alert.html', {'completed' : completed})



def testFriends(request):
    completed = None
    
    try:
        user = User.objects.exclude(is_superuser=1)

        query = 'SELECT max(id) as mid FROM auth_user'
        nusers = db_query(request, query)
        for i in nusers:
            v = int(i['mid'])

    #friends

        for u in user:
            nfr = random.randint(1, 20)
            nfrie = range(1,nfr)
            for f in nfrie:
                vicino = random.randint(1, 14)
                if (vicino == 1 or vicino == 2 or vicino == 13 or vicino == 14):
                   prof = Profilo.objects.get(user = u)
                   query = 'SELECT auth_user.id FROM auth_user, film_profilo where auth_user.id = film_profilo.user_id AND is_superuser <> 1 AND film_profilo.paese <> %s group by rand() limit 1'

                   ux = db_query_params(request, query, prof.paese)

                   for t in ux:
                       us = User.objects.get(id = t['id'])



                   presentesx = Amicizia.objects.filter(user=u, amico=us)
                   presentedx = Amicizia.objects.filter(user=us, amico=u)
                   if((len(presentesx) == 0) and (len(presentedx) == 0) and u.id != us.id):
                                       inserimento = Amicizia(user=u, amico=us, confermata=1)
                                       inserimento.save()
                if(vicino == 7 or vicino == 3 or vicino == 4 or vicino == 5 or vicino == 6):
                          prof = Profilo.objects.get(user = u)
                          query = 'SELECT auth_user.id FROM auth_user inner join film_profilo on auth_user.id = film_profilo.user_id where film_profilo.paese = %s AND auth_user.is_superuser <> 1 group by rand() limit 1'
                          par = [prof.paese]
                          ux = db_query_params(request, query, par)

                          for t in ux:
                              us = User.objects.get(id = t['id'])

                          presentesx = Amicizia.objects.filter(user=u, amico=us)
                          presentedx = Amicizia.objects.filter(user=us, amico=u)
                          if((len(presentesx) == 0) and (len(presentedx) == 0) and u.id != us.id):
                                              inserimento = Amicizia(user=u, amico=us, confermata=1)
                                              inserimento.save()

                if(vicino == 11 or vicino == 8 or vicino == 9 or vicino == 10 or vicino == 12):
                          prof = Profilo.objects.get(user = u)
                          query = 'SELECT auth_user.id FROM auth_user inner join film_profilo on auth_user.id = film_profilo.user_id where film_profilo.citta = %s AND auth_user.is_superuser <> 1 group by rand() limit 1'
                          par = [prof.citta]
                          ux = db_query_params(request, query, par)

                          for t in ux:
                              us = User.objects.get(id = t['id'])

                          presentesx = Amicizia.objects.filter(user=u, amico=us)
                          presentedx = Amicizia.objects.filter(user=us, amico=u)
                          if((len(presentesx) == 0) and (len(presentedx) == 0) and u.id != us.id):
                                              inserimento = Amicizia(user=u, amico=us, confermata=1)
                                              inserimento.save()

                completed = "Test completed"
    except:
           delet = Amicizia.objects.all().delete()  
           completed = "Test failed"

    return render_to_response('admin/alert.html', {'completed' : completed})




def testFollower(request):

    try:
        completed = None
        user = User.objects.exclude(is_superuser=1)

        query = 'SELECT max(id) as mid FROM auth_user'
        nusers = db_query(request, query)
        for i in nusers:
            v = int(i['mid'])

    #following
        for u in user:
            nf = random.randint(1, 10)
            nfoll = range(1,nf)
            for f in nfoll:

                query = 'SELECT auth_user.id FROM auth_user, film_profilo where auth_user.id = film_profilo.user_id AND is_superuser <> 1 group by rand() limit 1'

                ux = db_query(request, query)

                for t in ux:
                    us = User.objects.get(id = t['id'])

                presente = Follower.objects.filter(user=u, followed=us)

                if((len(presente) == 0) and u.id != us.id):
                                  inserimento = Follower(user=u, followed=us)
                                  inserimento.save()
        mostfollow = get_mostfollowed(request)

        for u in mostfollow:
            nf = random.randint(10, 20)
            nfoll = range(1,nf)
            for f in nfoll:
                query = 'SELECT auth_user.id FROM auth_user, film_profilo where auth_user.id = film_profilo.user_id AND auth_user.id <> %s AND is_superuser <> 1 group by rand() limit 1'
                ux = db_query_params(request, query, u['id'])
                for t in ux:
                    us = User.objects.get(id = t['id'])
                us2 = User.objects.get(id = u['id'])
                presente = Follower.objects.filter(user=us, followed=us2)


                if((len(presente) == 0) and us2.id != us.id):
                                  inserimento = Follower(user=us, followed=us2)
                                  inserimento.save()
        completed = "Test completed"
    except:
           delet = Follower.objects.all().delete()         
           completed = "Test failed"
    return render_to_response('admin/alert.html', {'completed' : completed})

    
def testGroups(request):
    completed = None
    
    try:
        onetoten = range(1,31)
        count = 0

        query = 'SELECT max(id) as mid FROM auth_user'
        nusers = db_query(request, query)
        for i in nusers:
            v = int(i['mid'])

        for count in onetoten:

            groupname = "group" + str(count)
            count = count + 1
            descrizione = 'desc'
            usid = random.randint(1, v)
            us = User.objects.get(id=usid)

            group = Group.objects.create(name=groupname)
            group.save()
            groupid = Group.objects.get(name = groupname)
            inserimento = ProfiloGruppo(user=us, group=groupid, descrizione = descrizione)
            inserimento.save()
            inserimento = Iscrizione(user=us, group = groupid)
            inserimento.save()
            completed = "Test completed"
    except:
           completed= "Test Failed"

    return render_to_response('admin/alert.html', {'completed' : completed})
    
    
    
def testIscriptions(request):
    completed = None

    try:
        user = User.objects.exclude(is_superuser=1)

        query = 'SELECT max(id) as mid FROM auth_group'
        nugroup = db_query(request, query)
        for i in nugroup:
            v = int(i['mid'])

    #following
        for u in user:
            ng = random.randint(1, 5)
            ngr = range(1,ng)
            for g in ngr:
                val = random.randint(1, v)
                gr = Group.objects.get(id = val)

                presente = Iscrizione.objects.filter(user=u, group=gr)

                if(len(presente) == 0):
                                 inserimento = Iscrizione(user=u, group=gr)
                                 inserimento.save()

        completed = "Test completed"

    except:
           delet = Iscrizione.objects.all().delete()
           completed = "Test failed"

    return render_to_response('admin/alert.html', {'completed' : completed})
    


def testTopics(request):
    completed = None

    try:
        groups = Group.objects.all()
        count = 0

        query = 'SELECT max(id) as mid FROM auth_user'
        nusers = db_query(request, query)
        for i in nusers:
            v = int(i['mid'])

        for g in groups:
            nt = random.randint(1, 20)
            nto = range(1,nt)

            for top in nto:
                descrizione = "topic" + str(count)
                count = count + 1

                query = 'SELECT auth_user.id FROM auth_user, film_iscrizione WHERE film_iscrizione.user_id = auth_user.id AND film_iscrizione.group_id = %s group by rand() limit 1'
                usx = db_query_params(request, query, g.id)

                for t in usx:
                    us = User.objects.get(id=t['id'])


                inserimento = Topic(user=us, group=g, descrizione = descrizione)
                inserimento.save()



        completed = "Test completed"
    except:
           completed = "Test failed"
    return render_to_response('admin/alert.html', {'completed' : completed})



def test(request):

    return render_to_response('admin/test.html', {})
    
    
def dbStatus(request):
    user = User.objects.exclude(is_superuser=1)
    result  =[]
    resultf =[]

    for u in user:

        amici = get_user_friends(request, u.id)
        amici.insert(0, u)
        result.append(amici)
        follower = get_followed(request, u.id)
        follower.insert(0, u)
        resultf.append(follower)

    return render_to_response('admin/status.html', {'result' : result, 'resultf' : resultf})