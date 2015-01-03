from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from ritazevallos.blog.models import Tag, Node, Path, PathNodeRelationship, Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ritazevallos.blog.forms import PathForm
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
                return HttpResponseRedirect(reverse('nodes_by_path', kwargs={'path_id': path.id}))
        else:
            form = PathForm(instance=path)
            return render(request, "path_form.html", {
                'form': form,
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
                return HttpResponseRedirect(reverse('nodes_by_path', kwargs={'path_id': path.id}))
        else:
            form = PathForm()
        return render(request, "path_form.html", {
            'form': form,
        })
    else:
        return HttpResponseRedirect(reverse('index'))

def nodes(request):
    node_list = Node.objects.all()
    paginator = Paginator(node_list, 10) # Show 10 nodes per page
    page = request.GET.get('page')
    try:
        nodes = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        # If page is not an integer, deliver first page.
        nodes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        nodes = paginator.page(paginator.num_pages)
    # using paginator https://docs.djangoproject.com/en/dev/topics/pagination/
    return render(request, "nodes.html", {
	    'nodes': nodes,
	    })

def nodes_by_tag(request,tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    node_list = Node.objects.filter(tags__id = tag.id)
    paginator = Paginator(node_list, 10) # Show 10 nodes per page
    page = request.GET.get('page')
    try:
        nodes = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        # If page is not an integer, deliver first page.
        nodes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        nodes = paginator.page(paginator.num_pages)
    return render(request, "nodes.html", {
        'title': tag.name,
		'nodes': nodes,
		})

def helper_by_path(request,path_id):
    path = get_object_or_404(Path, id=path_id)
    #if path_id == 1: # projects
    return render(request, "projects_helper.html")

def nodes_by_path(request,path_id):
    path = get_object_or_404(Path, id=path_id)
    node_list = path.nodes.all()
    paginator = Paginator(node_list, 10) # Show 10 nodes per page
    page = request.GET.get('page')
    try:
        nodes = paginator.page(page)
    except (PageNotAnInteger, TypeError):
        # If page is not an integer, deliver first page.
        nodes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        nodes = paginator.page(paginator.num_pages)
    return render(request, "nodes.html", {
        'title': path.title,
		'nodes': nodes,
		})

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
	return render(request, "node.html", { 'node': node, })