from django.conf.urls.defaults import patterns, url
from ritazevallos.blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^projects$', views.projects, name='projects'),
    url(r'^node/(?P<node_id>\d+)/$', views.node, name="node"),
    url(r'^path/new', views.new_path, name="new_path"),
    url(r'^node/new$', views.new_node, name="new_node"),
    url(r'^node/(?P<node_id>\d+)/edit$', views.edit_node, name="edit_node"),
    url(r'^path/(?P<path_id>\d+)/edit$', views.edit_path, name="edit_path"),
    url(r'^path/(?P<path_id>\d+)/$', views.nodes_by_path, name='nodes_by_path'),
    url(r'^tag/(?P<tag_id>\d+)/$', views.paths_by_tag, name='tag'),
    url(r'^autocomplete_nodes', views.autocomplete_nodes, name='autocomplete_nodes'),
    url(r'^graph', views.load_graph, name='load_graph'),
    url(r'^helper/(?P<path_id>\d+)/$', views.helper_by_path, name='helper'),
    url(r'^convert_n2p/(?P<node_id>\d+)/$', views.convert_node_to_path, name='convert_node_to_path'),
    )