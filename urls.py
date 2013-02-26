from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from film.views import *
admin.autodiscover()
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Example:
    # (r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
(r'^admin/', include(admin.site.urls)),



(r'^$',  "film.v_home.login_h"),
(r'^accounts/login/$',  "film.v_home.login_h"),
(r'^accounts/logout/$', "film.v_home.logout_h"),
(r'^accounts/register/$', "film.views_users.register"),
(r'^confirm/(\w+)/(\w+)$', "film.views_users.confirm"),


# pagina di ricerca

(r'^film/tot/$', "film.views.films"), #tutti i film nel db

(r'^accounts/profile/$', "film.views_imdb.ricerca"),
(r'^accounts/profile/myprofile/$', "film.views_profile.myprofile"),
(r'^accounts/profile/myprofile/chpswd/$', "film.views_profile.change_passwd"),
(r'^accounts/profile/myprofile/image/$', "film.views_profile.upload_image"),



(r'^search/$', "film.v_search.searchGlobal"),

#update
(r'^upd_trailer$', "film.v_tmdb.upd_trailer"),


#azioni utenti
(r'^film/ricerca/imdb/(\d+)/$', "film.views_imdb.imdb"),
(r'^film/select/$', "film.views_search.selectFilm"),

(r'^film/select/director/$', "film.views_search.selectDir"),
(r'^film/select/director/(\d+)/$', "film.views_search.filmDir"),

(r'^film/select/genre/$', "film.views_search.selectGen"),
(r'^film/select/genre/(\d+)/$', "film.views_search.filmGen"),

(r'^film/select/actor/$', "film.views_search.selectAct"),
(r'^film/select/actor/(\d+)/$', "film.views_search.filmAct"),

(r'^film/inserisci/(\w+)/$', "film.v_tmdb.insert_tmdb"),
(r'^film/test/$', "film.v_IMDB.test"),

(r'^film/scheda/(\d+)/$', "film.views_film.scheda"),
(r'^film/scheda/cast/(\d+)/$', "film.views_film.cast"),
(r'^film/scheda/completa/(\d+)/$', "film.views_film.schedaimdb"),
(r'^film/scheda/vota/(\d+)/$', "film.views_film.rating"),
(r'^film/scheda/commenti/(\d+)/$', "film.views_film.inserisciCommento"),


#url gestione preferiti
(r'^film/inspreferiti/(\d+)/$', "film.views_film.insPreferiti"),
(r'^film/showpreferiti/(\d+)/$', "film.views_film.showPreferiti"),
(r'^film/showPref/(\d+)/$', "film.views_film.showPref"),


(r'^fav/genre/(\d+)/$', "film.views_film.insFavGen"),
(r'^fav/actor/(\d+)/$', "film.views_film.insFavAct"),
(r'^fav/dir/(\d+)/$', "film.views_film.insFavDir"),

#utenti
(r'^utenti/select/$', "film.views_users.selectUser"),
(r'^utenti/select/filter/$', "film.views_users.filterUser"),
(r'^utenti/amicizia/tot/(\d+)/$', "film.views_users.amici"),
(r'^utenti/profilo/(\d+)/$', "film.views_users.profilo"),
(r'^utenti/profilo/amici/(\d+)/$', "film.views_users.amiciUser"),
(r'^utenti/amicizia/(\d+)/$', "film.views_users.amicizia"),
(r'^utenti/amicizia/conferma/(\d+)/$', "film.views_users.conferma"),
(r'^utenti/amicizia/rifiuta/(\d+)/$', "film.views_users.rifiuta"),


(r'^utenti/follow/(\d+)/$', "film.views_followers.follow"),
(r'^utenti/follow/tot/(\d+)/$', "film.views_followers.allFollow"),
(r'^utenti/follow/actions/(\d+)$', "film.views_followers.actions"),
(r'^utenti/follower/tot/(\d+)/$', "film.views_followers.allFollower"),

#gruppi
(r'^gruppi/$', "film.views_groups.insGruppo"),
(r'^gruppi/select/$', "film.views_groups.selectGruppo"),
(r'^gruppi/topics/(\d+)/$', "film.views_groups.topics"),
(r'^gruppi/iscrizione/(\d+)/$', "film.views_groups.subscribe"),

#topic
(r'^topic/insert/(\d+)/$', "film.views_groups.instopic"),
(r'^topic/(\d+)/$', "film.views_groups.showTopic"),




#URLS DI DI FUNZIONI DI CANCELLAZIONE
(r'^users/friends/delete/(\d+)/$', "film.views_del.delete_friend"),
(r'^users/follow/delete/(\d+)/$', "film.views_del.delete_follow"),

(r'^film/fav/delete/(\d+)/$', "film.views_del.delete_fav"),
(r'^groups/delete/sub/(\d+)/$', "film.views_del.delete_sub"),
(r'^groups/delete/(\d+)/$', "film.views_del.delete_group"),

(r'^login/admin/$', "film.views_admin.login"),
(r'^adm/home/$', "film.views_admin.home"),
(r'^adm/reptop/$', "film.views_admin.reportedTopicComments"),
(r'^adm/repc/$', "film.views_admin.reportedComments"),
(r'^adm/profile/(\d+)/$', "film.views_admin.userProfile"),
(r'^adm/deleteUser/(\d+)/$', "film.views_admin.userDelete"),
(r'^adm/deleteComment/(\d+)/$', "film.views_admin.commentDelete"),
(r'^adm/deleteTopComment/(\d+)/$', "film.views_admin.commentTopDelete"),

(r'^report/topic/(\d+)/$', "film.views_groups.reportTopic"),
(r'^report/(\d+)/$', "film.views_film.report"),

#test
(r'^test/$', "film.views_test.test"),
(r'^test/users/$', "film.views_test.testUsers"),
(r'^test/fav/$', "film.views_test.testFav"),
(r'^test/friends/$', "film.views_test.testFriends"),
(r'^test/follower/$', "film.views_test.testFollower"),
(r'^test/groups/$', "film.views_test.testGroups"),
(r'^test/iscr/$', "film.views_test.testIscriptions"),
(r'^test/topics/$', "film.views_test.testTopics"),

(r'^db/status/$', "film.views_test.dbStatus"),
 (r'^film/', include('film.urls')),
)


urlpatterns += staticfiles_urlpatterns()
