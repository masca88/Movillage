# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from models import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from mylib import *


@login_required(login_url='/accounts/login/')
def films(request):
    film = Film.objects.all().order_by('titolo')
    posts = pagination(request, film, 10)
    return render_to_response("film/libreria.html", dict(posts=posts, user=request.user))

@login_required(login_url='/accounts/login/')
def film(request, id):
    try:
        film = Film.objects.get(pk=id)
        return HttpResponse("'%s'<br>" % (film.titolo))
    except Film.DoesNotExist:
           return HttpResponse("Codice %s inesistente" % id)


