from django.conf.urls.defaults import patterns, url
from ritazevallos.blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^projects$', views.projects, name='projects'),
    url(r'^thoughts$', views.thoughts, name='thoughts'),
    url(r'^stories$', views.stories, name='stories'),
    url(r'^node/(?P<node_id>\d+)/$', views.node, name="node"),
    url(r'^new_path$', views.new_path, name="new_path"),
    url(r'^path/(?P<tag_id>\d+)/edit$', views.edit_path, name="edit_path"),
    url(r'^tag/(?P<tag_id>\d+)/$', views.nodes_by_tag, name='nodes_by_tag'),
    url(r'^path/(?P<path_id>\d+)/$', views.nodes_by_path, name='nodes_by_path'),
    url(r'^nodes$', views.nodes, name='nodes'),
    url(r'^idea_book', views.all_external, name='all_external'),
    url(r'^autocomplete_nodes', views.autocomplete_nodes, name='autocomplete_nodes'),
    )