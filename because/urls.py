from django.conf.urls.defaults import patterns, url
from ritazevallos.because import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^complete/(?P<beginning_id>\d+)/$', views.complete, name='complete_form'),
    url(r'^begin/$', views.beginning, name='beginning_form'),
    url(r'^ending/(?P<ending_id>\d+)/$', views.ending, name='ending'),
    url(r'^beginnings/$', views.beginnings, name='beginnings'),
    url(r'^endings/$', views.endings, name='endings'),
    )