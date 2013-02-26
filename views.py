from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
def hello(request):
	return HttpResponse("Hello world")
	
	
	

