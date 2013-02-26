from django.db import models
from django.contrib.auth.models import *
# Create your models here.
from datetime import datetime, date

class Paese(models.Model):
	descrizione = models.CharField(max_length=30)
	def __unicode__(self):
            return self.descrizione
	class Meta:
              verbose_name_plural = "Paesi"
              
class Compagnia(models.Model):
	descrizione = models.CharField(max_length=100)
	def __unicode__(self):
            return self.descrizione
	class Meta:
              verbose_name_plural = "Compagnia"

class Lingua(models.Model):
	descrizione = models.CharField(max_length=30)
	def __unicode__(self):
            return self.descrizione
	class Meta:
              verbose_name_plural = "Lingue"

class Regista(models.Model):
	nome = models.CharField(max_length=50)
	def __unicode__(self):
            return self.nome
	class Meta:
              verbose_name_plural = "Registi"

class Scrittore(models.Model):
	nome = models.CharField(max_length=50)
	def __unicode__(self):
            return self.nome
	class Meta:
              verbose_name_plural = "Scrittore"


class Genere(models.Model):
	descrizione = models.CharField(max_length=30)
	def __unicode__(self):
            return self.descrizione
	class Meta:
              verbose_name_plural = "Generi"

class Attore(models.Model):
	nome = models.CharField(max_length=50)
	def __unicode__(self):
            return self.nome
	class Meta:
              verbose_name_plural = "Attori"
              
class Personaggio(models.Model):
	descrizione = models.CharField(max_length=100)
	def __unicode__(self):
            return self.descrizione
	class Meta:
              verbose_name_plural = "Personaggi"


class Film(models.Model):
	titolo = models.CharField(max_length=200)
	trama = models.TextField(null=True, blank=True)
	cover = models.URLField(max_length=500, null=True, blank=True)
	anno = models.IntegerField(null=True, blank=True)
	imdbId = models.CharField(max_length=30)
	trailer = models.CharField(max_length=30, blank=True)
	date = models.DateField(default=datetime.now, blank=True)
	def __unicode__(self):
            return self.titolo
	class Meta:
              verbose_name_plural = "Film"

class Filmcast(models.Model):
	film = models.ForeignKey(Film)
	attore = models.ForeignKey(Attore)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.attore)
	class Meta:
              verbose_name_plural = "Filmcast"
              
              
class Regia(models.Model):
	film = models.ForeignKey(Film)
	regista = models.ForeignKey(Regista)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.regista)
	class Meta:
              verbose_name_plural = "Regia"


class Scrive(models.Model):
	film = models.ForeignKey(Film)
	scrittore = models.ForeignKey(Scrittore)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.scrittore)
	class Meta:
              verbose_name_plural = "Scrittore"
              
class Set(models.Model):
	film = models.ForeignKey(Film)
	paese = models.ForeignKey(Paese)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.paese)
	class Meta:
              verbose_name_plural = "Set"
              
class LinguaFilm(models.Model):
	film = models.ForeignKey(Film)
	lingua = models.ForeignKey(Lingua)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.lingua)
	class Meta:
              verbose_name_plural = "Lingua Film"
              
class CompagniaFilm(models.Model):
	film = models.ForeignKey(Film)
	compagnia = models.ForeignKey(Compagnia)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.compagnia)
	class Meta:
              verbose_name_plural = "Compagnia Film"
              
class GenereFilm(models.Model):
	film = models.ForeignKey(Film)
	genere = models.ForeignKey(Genere)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.genere)
	class Meta:
              verbose_name_plural = "Genere Film"

class Compare(models.Model):
	film = models.ForeignKey(Film)
	personaggio = models.ForeignKey(Personaggio)
	attore = models.ForeignKey(Attore)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.personaggio)
	class Meta:
              verbose_name_plural = "Compare"

class Preferito(models.Model):
	utente = models.ForeignKey(User, on_delete=models.CASCADE)
	film = models.ForeignKey(Film)
	def __unicode__(self):
            return u"%s %s" % (self.film, self.utente)
	class Meta:
              verbose_name_plural = "Preferiti"
              
class GenerePreferito(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        genere = models.ForeignKey(Genere)

class AttorePreferito(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        attore = models.ForeignKey(Attore)

class RegistaPreferito(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        regista = models.ForeignKey(Regista)

class Voto(models.Model):
        rating = models.IntegerField()
	utente = models.ForeignKey(User, on_delete=models.CASCADE)
	film = models.ForeignKey(Film)
	def __unicode__(self):
            return self.rating
	class Meta:
              verbose_name_plural = "Voti"

class Commento(models.Model):
        commento = models.TextField()
	utente = models.ForeignKey(User, on_delete=models.CASCADE)
	film = models.ForeignKey(Film)
	date = models.DateTimeField(default=datetime.now)
	reported = models.BooleanField(default=False)
	def __unicode__(self):
            return self.commento
	class Meta:
              verbose_name_plural = "Commenti"



class Profilo(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        nome = models.CharField(max_length=30)
        cognome = models.CharField(max_length=30)
        paese = models.CharField(max_length=30, null=True, blank=True)
        citta = models.CharField(max_length=30, null=True, blank=True)
        eta = models.DateField()
        gender = models.CharField(max_length=1,null=True, blank=True)
        name = models.CharField(max_length=300, null=True, blank=True, default="avatar.jpg")
        reported = models.BooleanField(default=False)
        confirmation_code = models.CharField(max_length=30, null=True, blank=True)

class Amicizia(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        amico = models.ForeignKey(User, related_name='user')
        confermata = models.BooleanField(default=False)
        date = models.DateField(default=datetime.now)

class ProfiloGruppo(models.Model):
        group = models.ForeignKey(Group)
        descrizione =  models.TextField()
        date = models.DateField(default=datetime.now)
        user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
        reported = models.BooleanField(default=False)

class Topic(models.Model):
        descrizione = models.CharField(max_length=300)
        group = models.ForeignKey(Group)
        date = models.DateField(default=datetime.now)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        reported = models.BooleanField(default=False)

class Iscrizione(models.Model):
        group = models.ForeignKey(Group)
        date = models.DateField(default=datetime.now)
        user = models.ForeignKey(User, on_delete=models.CASCADE)

class TopicCommento(models.Model):
        topic = models.ForeignKey(Topic)
        date = models.DateTimeField(default=datetime.now)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        commento = models.TextField()
        reported = models.BooleanField(default=False)

class Follower(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        followed = models.ForeignKey(User, related_name='followed')
        date = models.DateField(default=datetime.now)





