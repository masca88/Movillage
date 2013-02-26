import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from mylib import *
from myfunct import *
from classes import *



@csrf_protect
@never_cache
def login(request, template_name='admin/loginAdmin.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    admin = get_superuser(request)
    fail = None
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        username = request.POST.get('username')
        
        if username != admin.username:
            fail = 1
            return render_to_response('admin/loginAdmin.html', {'fail' : fail, 'form' : form})

        if form.is_valid():

            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))




def home(request):



    return render_to_response('admin/home.html', {})
    
    
def reportedComments(request):

    query = 'select film_commento.commento, film_commento.date, film_commento.id as commento_id, auth_user.id, auth_user.username from film_commento, film_profilo, auth_user where auth_user.id = film_profilo.user_id AND film_profilo.user_id = film_commento.utente_id AND film_commento.reported = 1 ORDER by film_commento.date DESC'
    result = db_query(request, query)
    
    if(len(result) == 0):
                   conferma = "No comment reported"
                   return render_to_response('admin/alert.html', {'completed' : conferma})
           #cerca se ci sono richieste di amicizia non confermate
    posts = pagination(request, result, 5)
    return render_to_response('admin/commentsReported.html', {'posts' : posts})
    
    
    
def reportedTopicComments(request):

    query = 'select film_topiccommento.id as commento_id, film_topiccommento.commento, film_topiccommento.date, auth_user.username, auth_user.id from film_topiccommento, film_profilo, auth_user where auth_user.id = film_profilo.user_id AND film_profilo.user_id = film_topiccommento.user_id AND film_topiccommento.reported = 1 ORDER by film_topiccommento.date DESC'
    result = db_query(request, query)
    posts = pagination(request, result, 5)
    
    if(len(result) == 0):
                   conferma = "No comment reported"
                   return render_to_response('admin/alert.html', {'completed' : conferma})
           #cerca se ci sono richieste di amicizia non confermate
    posts = pagination(request, result, 5)
    return render_to_response('admin/commentsTopReported.html', {'posts' : posts})


def userProfile(request, id):

    user = User.objects.get(id=id)
    profile = Profilo.objects.get(user = id)

    return render_to_response('admin/userProfile.html', {'user' : user, 'profile': profile})
    
    
    
def userDelete(request, id):

    user = User.objects.get(id=id).delete()

    conferma = "User deleted"
    return render_to_response('admin/alert.html', {'completed' : conferma})

def commentDelete(request, id):

    c = Commento.objects.get(id=id).delete()

    conferma = "Comment deleted"
    return render_to_response('admin/alert.html', {'completed' : conferma})
    
    
def commentTopDelete(request, id):

    tc = TopicCommento.objects.get(id=id).delete()

    conferma = "Comment deleted"
    return render_to_response('admin/alert.html', {'completed' : conferma})


