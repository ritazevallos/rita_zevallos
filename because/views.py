from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from ritazevallos.because.models import Beginning, Ending
from ritazevallos.because.forms import BeginningForm, EndingForm
from django.utils import simplejson
import json

def index(request):
    endings = Ending.objects.all()
    # beginnings = Beginning.objects.all()
    beginnings = Beginning.objects.exclude(id__in=[elem.beginning.id for elem in Ending.objects.all()])
    return render(request, "because/index.html", {
        'endings': endings,
        'beginnings': beginnings,
        })

# todo: paginate these three views
def endings(request):
    endings = Ending.objects.all()
    ending_id_list = [str(id) for id in endings.values_list('id', flat=True)]
    # todo: request.is_ajax was returning false for some reason so I took it out
    return HttpResponse(json.dumps(ending_id_list), content_type="application/json")

def beginnings(request):
    # beginnings = Beginning.objects.all()
    beginnings = Beginning.objects.exclude(id__in=[elem.beginning.id for elem in Ending.objects.all()])
    beginning_id_list = [str(id) for id in beginnings.values_list('id', flat=True)]
    return HttpResponse(json.dumps(beginning_id_list), content_type="application/json")

def beginning(request):
    if request.method == "POST":
        form = BeginningForm(request.POST)
        if form.is_valid():
            beginning = form.save()
            data = { 'beginning_id': beginning.id }
            if request.is_ajax():
                return HttpResponse(simplejson.dumps(data), content_type="application/json")
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        form = BeginningForm()
    return render(request, "because/beginning_form.html", {'form':form})

def ending(request,ending_id):
    ending = get_object_or_404(Ending,id=ending_id)
    beginning = ending.beginning
    return render(request, "because/_show.html", {
        'beginning': beginning,
        'ending': ending })

def complete(request,beginning_id):
    beginning = get_object_or_404(Beginning,id=beginning_id)
    if request.method == "POST":
        form = EndingForm(request.POST)
        if form.is_valid():
            ending = form.save()
            data = {'ending_id': ending.id}
            if request.is_ajax():
                return HttpResponse(simplejson.dumps(data), content_type="application/json")
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        form = EndingForm(initial={"beginning":beginning_id})
    return render(request, "because/complete_form.html", {'beginning':beginning, 'form':form})