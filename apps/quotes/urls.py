from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^quotes$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^quotes/add_quote$', views.add_quote),
    url(r'^quotes/(?P<quote_id>\d+)/add_favorite$', views.add_favorite),
    url(r'^quotes/(?P<quote_id>\d+)/remove_favorite$', views.remove_favorite),
    url(r'^user/(?P<user_id>\d+)$', views.user),
]
