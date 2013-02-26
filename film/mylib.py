import MySQLdb
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from models import *
from django.contrib.sessions.models import *
from django.contrib.auth.models import *
from settings import *
from django.conf import settings
import random

#funzione per la gestione dei risultati delle queries


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    

#disable csrf

class DisableCSRF(object):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        

#funzione per la paginazione

def pagination(request, lista, k):
    paginator = Paginator(lista, k)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1
    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return posts
    



#restituisce l'utente loggato

def get_user(request):
    session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user=0
    return user

#restituisce id utente loggato

def get_uid(request):
    session_key = request.COOKIES[settings.SESSION_COOKIE_NAME]
    session = Session.objects.get(session_key=session_key)
    uid = session.get_decoded().get('_auth_user_id')
    return uid


#connessione e query alla bd

def db_query(request, query):

    db = DATABASES['default']
    dbname = db['NAME']
    dbpasswd = db['PASSWORD']
    dbuser = db['USER']
    dbhost = db['HOST']

    db = MySQLdb.connect(user=dbuser, db=dbname, passwd=dbpasswd, host=dbhost)
    cursor = db.cursor()
    cursor.execute(query)
    results = dictfetchall(cursor)
    db.close()

    return results



def db_query_params(request, query, params):

    db = DATABASES['default']
    dbname = db['NAME']
    dbpasswd = db['PASSWORD']
    dbuser = db['USER']
    dbhost = db['HOST']

    db = MySQLdb.connect(user=dbuser, db=dbname, passwd=dbpasswd, host=dbhost)
    cursor = db.cursor()
    cursor.execute(query, params)
    results = dictfetchall(cursor)
    db.close()

    return results




def elimina_doppioni(request, lista):
    for i in lista:                          #elimina i doppioni
        if lista.count(i) > 1:
            lista.remove(i)
            
    return lista

def get_superuser(request):

    result = User.objects.get(is_superuser=1)

    return result
    
    
def get_random_word(request, wordLen):
    word = ''
    for i in range(wordLen):
        word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    return word


from random import randrange
from datetime import timedelta, datetime
import datetime


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second)).strftime("%Y-%m-%d")



def get_random_imdbId(request):
    word = ''
    for i in range(9):
        word += random.choice('0123456789')
    return word

    
    
    

