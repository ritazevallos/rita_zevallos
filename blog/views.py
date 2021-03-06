from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from ritazevallos.blog.models import Tag, Node, Path, PathNodeRelationship, Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ritazevallos.blog.forms import PathForm, NodeForm
import json
from django.core import serializers

def index(request):
	return render(request, "index.html", {'landing': True,})

def load_graph(request):
    json_nodes = serializers.serialize("json", Node.objects.all())
    json_links = serializers.serialize("json", Link.objects.all())
    data = {
        'nodes': json_nodes,
        'links': json_links,
        }
    return HttpResponse(json.dumps(data), content_type="application/json")

def convert_node_to_path(request,node_id):
    if request.user.is_superuser:
        node = get_object_or_404(Node,id=node_id)
        path = node.convert_to_path() # will either get the existent path w this name, or a new created one
        return HttpResponseRedirect(reverse('edit_path', kwargs={'path_id': path.id, 'base_template':"base.html"}))
    else:
        return HttpResponseRedirect(reverse('index'))

def edit_node(request, node_id):
    if request.user.is_superuser:
        node = get_object_or_404(Node, id=node_id)
        if request.method == "POST":
            form = NodeForm(request.POST,instance=node)
            if form.is_valid():
                node = form.save()
                data = { 'node_id': node.id }
            else:
                data = { 'errors': form.errors }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            form = NodeForm(instance=node)
        return render(request, "node_form.html", {
            'form': form,
            'base_template': 'base.html',
            })
    else:
        return HttpResponseRedirect(reverse('index'))

def edit_path(request, path_id):
    if request.user.is_superuser:
        path = get_object_or_404(Path, id=path_id)
        if request.method == "POST":
            form = PathForm(request.POST,instance=path)
            if form.is_valid():
                path = form.save(commit=False)
                path.save()
                path.nodes.clear()
                index = 1
                for node in form.cleaned_data.get('nodes'):
                    pathNodeRelationship = PathNodeRelationship(path=path, node=node)
                    pathNodeRelationship.order_index = index
                    pathNodeRelationship.save()
                    index += 1
                path.save() # save the links too
                return HttpResponseRedirect(reverse('nodes_by_path', kwargs={'path_id': path.id, 'base_template':'base.html'}))
        else:
            form = PathForm(instance=path)
            return render(request, "path_form.html", {
                'form': form,
                'base_template': 'base.html',
                })
    else:
        return HttpResponseRedirect(reverse('index'))

def new_node(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = NodeForm(request.POST)
            if form.is_valid():
                node = form.save()
                data = {
                    'node_id': node.id,
                    'node_str': str(node)
                }
            else:
                data = { 'errors': form.errors }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            form = NodeForm()
        return render(request, "node_form.html", {
            'form': form,
            'base_template': 'base_ajax.html',
            })
    else:
        return HttpResponseRedirect(reverse('index'))

def new_path(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = PathForm(request.POST)
            if form.is_valid():
                path = form.save(commit=False)
                path.save()
                index = 1
                for node in form.cleaned_data.get('nodes'):
                    pathNodeRelationship = PathNodeRelationship(path=path, node=node)
                    pathNodeRelationship.order_index = index
                    pathNodeRelationship.save()
                    index += 1
                path.save() # save the links too
                kwargs = {
                    'path_id': path.id,
                    'base_template': 'base.html'
                    }
                return HttpResponseRedirect(reverse('nodes_by_path', kwargs))
        else:
            form = PathForm()
        return render(request, "path_form.html", {
            'form': form,
            'base_template': 'base.html'
        })
    else:
        return HttpResponseRedirect(reverse('index'))

def delete_node(request,node_id):
    if request.user.is_superuser:
        node = get_object_or_404(Node, id=node_id)
        if node.delete():
            success=True
        else:
            success=False
        return HttpResponse(json.dumps({'success':success}), content_type="application/json")
    else:
        return HttpResponseRedirect(reverse('index'))

def remove_node_from_path(request,path_id,node_id):
    if request.user.is_superuser:
        path = get_object_or_404(Path, id=path_id)
        node = get_object_or_404(Node, id=node_id)
        rel = get_object_or_404(PathNodeRelationship, path=path, node=node)
        if rel.delete():
            success=True
        else:
            success=False
        return HttpResponse(json.dumps({'success':success}), content_type="application/json")
    else:
        return HttpResponseRedirect(reverse('index'))

def helper_by_path(request,path_id):
    path = get_object_or_404(Path, id=path_id)
    if path.id == 1: # projects
        return render(request, "projects_helper.html")
    elif path.id == 2: # wip projects
        return render(request, "projects_wip_helper.html")
    else:
        return render(request, "projects_helper.html")

def paths_by_tag(request,tag_id):
    tag = get_object_or_404(Tag,id=tag_id)
    template = "tag_show.html"
    if request.is_ajax():
        base_template = "base_ajax.html"
    else:
        base_template = "base.html"
    paths = Path.objects.filter(tags__id = tag.id)
    data = {
        'title': tag.name,
		'paths': paths,
		'base_template': base_template,
	}
    return render(request, template, data)

def nodes_by_path(request,path_id):
    path = get_object_or_404(Path, id=path_id)
    template = "nodes.html"
    nodes = path.nodes.all()
    if request.is_ajax():
        base_template = "base_ajax.html"
    else:
        base_template = "base.html"
    data = {
        'title': path.title,
		'nodes': nodes,
		'base_template': base_template
		}
    return render(request, template, data)

def autocomplete_nodes(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        nodes = Node.objects.filter(title__icontains = q )[:20]
        results = []
        for node in nodes:
            drug_json = {}
            drug_json['id'] = node.id
            drug_json['title'] = node.title
            results.append(drug_json)
        data = json.dumps(results)
    else:
        data = 'fail. not ajax.'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def node(request, node_id):
	node = get_object_or_404(Node, id=node_id)
	if request.is_ajax():
	    base_template = 'base_ajax.html'
        else:
            base_template = 'base.html'
	return render(request, "node.html", {
	    'node': node,
	    'base_template': base_template,
	    })

def projects(request):
    if request.is_ajax():
        base_template = 'base_ajax.html'
    else:
        base_template = 'base.html'
    return render(request, "projects.html", {
        'base_template': base_template
        })