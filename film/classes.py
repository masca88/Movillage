from django import forms
from models import *
from datetime import datetime, date
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget


class filmcast():
      attore = ''
      personaggio = ''
      
      
      
class formCommento(forms.Form):
    commento = forms.CharField(widget=forms.Textarea, label= (u''))
    
    def __init__(self, *args, **kwargs):
        super(formCommento, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['commento'].widget.attrs['cols'] = 60
        
        
        
class rate(forms.Form):
    to_send_form = forms.ChoiceField(widget=forms.RadioSelect)



class creaGruppo(forms.Form):
    nome = forms.CharField(required=False, label= (u'Groupname'))
    desc = forms.CharField(required=False, widget=forms.Textarea, label= (u'Description'))


    def __init__(self, *args, **kwargs):
        super(creaGruppo, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['nome'].widget.attrs['cols'] = 60
        self.fields['desc'].widget.attrs['cols'] = 60
        
        
class ricercaGruppo(forms.Form):
    gruppo = forms.CharField(required=True, label= (u'Groupsearch'))
    
    
class formTopic(forms.Form):
    topic = forms.CharField(required=False, label= (u'Insert title here'))
    commento = forms.CharField(required=False, widget=forms.Textarea, label= (u'')) 


    def __init__(self, *args, **kwargs):
        super(formTopic, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['topic'].widget.attrs['cols'] = 60
        self.fields['commento'].widget.attrs['cols'] = 60
        
        


class formTopicComm(forms.Form):
    commento = forms.CharField(widget=forms.Textarea, label= (u''))
    
    def __init__(self, *args, **kwargs):
        super(formTopicComm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['commento'].widget.attrs['cols'] = 60




class ch_pass(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput,required=False, label= (u'Insert your old password'))
    new_password = forms.CharField(widget=forms.PasswordInput, required=False, label= (u'Insert new password'))
    new_password_conf = forms.CharField(widget=forms.PasswordInput, required=False, label= (u'Confirm new password'))



class ImageForm(forms.Form):
    image = forms.ImageField()
    
    
    
    
    
class ricercaFilm(forms.Form):
    film = forms.CharField(required=True)
    
    
class ricercaDir(forms.Form):
    director = forms.CharField(required=True)



class ricercaGen(forms.Form):
    genere = forms.CharField(required=True)
    

class ricercaAct(forms.Form):
    actor = forms.CharField(required=True)
    
    
    
class registrazione(forms.Form):
    GENDER_CHOICES = (('m', 'Male'), ('f', 'Female'))
    username = forms.CharField(required=False, label= (u'Username'))
    password = forms.CharField(widget=forms.PasswordInput, required=False, label= (u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, required=False, label= (u'Re-enter password'))
    email = forms.CharField(required=False,label= (u'eMail'))
    nome = forms.CharField(required=False,label= (u'First name'))
    cognome = forms.CharField(required=False,label= (u'Last name'))
    paese = forms.CharField(required=False,label= (u'Country'))
    citta = forms.CharField(required=False,label= (u'Hometown'))
    eta = forms.DateField(widget=SelectDateWidget(years=range(1950, 2000)), label= (u'Date of birth'))
    sex = ChoiceField(widget=RadioSelect, choices=GENDER_CHOICES)
    
    
    
#form ricerca utente
class ricercaUtente(forms.Form):
    username = forms.CharField(required=True, label= (u'Search user'))
    

#form ricerca utente
class filtraUtente(forms.Form):
    GENDER_CHOICES = (('m', 'Male'), ('f', 'Female'))
    country = forms.CharField(required=False, label= (u'Country'))
    hometown = forms.CharField(required=False, label= (u'Hometown'))
    sex = ChoiceField(required=False,widget=RadioSelect, choices=GENDER_CHOICES)
    
    
    
    
class formCommentoAdmin(forms.Form):
    commento = forms.CharField(widget=forms.Textarea, label= (u''))

    def __init__(self, *args, **kwargs):
        super(formCommentoAdmin, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['commento'].widget.attrs['cols'] = 60
        
        

class userprofile():
      user = ''
      profile = ''


class ricerca_TMDB(object):
    def __init__(self, title=None, r_date=None, tmdbID=None, poster=None):
        self.title = title
        self.r_date = r_date
        self.tmdbID = tmdbID
        self.poster = poster
    

    
    
    
    