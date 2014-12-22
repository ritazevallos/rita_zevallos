from django import template
from ritazevallos.blog.models import Link, Node
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder

register = template.Library()

@register.tag
def get_graph():
    graph = {}
    nodes_list=[]
    for node in Node.objects.all():
        record = {"id":node.id, "x":node.locationX, "y":node.locationY, "z":node.locationZ, }
        nodes_list.append(record)

    links_list = []
    for link in Link.objects.all():
        record = {"from_id":link.from_node.id, "to_id":link.to_node.id,}
        links_list.append(record)

    graph["links"]=links_list

    return json.dumps(graph, cls=DjangoJSONEncoder)