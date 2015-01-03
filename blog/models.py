from django.db import models
from django.db.models.signals import post_save

class Tag(models.Model):
	name = models.CharField(max_length=200, null=False, unique=True)

	def __unicode__( self ):
		return self.name

	""" Only call if converting for the first time, as it assumes that
	any existing tag_path does not need to be overridden.
	In the future, all nodes added to the tag should be added to the
	tag_path automatically."""
	def convert_to_path( self ):
	    title = self.name + " tag"
	    old_path = Path.objects.filter(title=title)
	    if not old_path:
	        path = Path(title=self.name)
	        path.save()
	        node_list = Node.objects.filter(tags__id = self.id)
	        for node in node_list:
	            rel = PathNodeRelationship(path=path, node=node,order_index = path.nodes.count())
	            rel.save()
            path.save()

class Node(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="post_tags",blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    private = models.BooleanField(default=False)
    external = models.BooleanField() # automatically set if link is empty/nonempty
    links = models.ManyToManyField('self', through='Link',
                                           symmetrical=False,
                                           related_name='related_to+')
    #pos = VectorField(blank=True, null=True);
    locationX = models.IntegerField(blank=True, null=True)
    locationY = models.IntegerField(blank=True, null=True)
    locationZ = models.IntegerField(blank=True, null=True)

    def __unicode__( self ):
        return self.title if self.title else "No title"

    def is_long ( self ):
        return (len(self.text) > 1000)

    def excerpt( self ):
        default_cutoff = 1000
        cutoff = min(len(self.text),default_cutoff)
        return self.text[:cutoff]

    def save(self, *args, **kwargs):
        super(Node, self).save(*args, **kwargs)
        if not self.link or self.link == "":
            self.external = False
        else:
            self.external = True
            idea_book = Tag.objects.get(name="IdeaBook")
            self.tags.add(idea_book)

        if self.tags:
            for tag in self.tags.all():
                tag_paths = Path.objects.filter(title=tag.name) # should be 1 or 0
                if tag_paths:
                    tag_path = tag_paths[0]
                else:
                    tag_path = Path(title=tag.name)
                rel = PathNodeRelationship(path=tag_path, node=self, order_index=tag_path.nodes.count())
                rel.save()
                tag_path.save() # do da links

            # THE BELOW DOESN'T WORK ON AN UNPAID PYTHONEVERYWHERE ACCOUNT
            # import urllib
            # from bs4 import BeautifulSoup
            # url = urllib.urlopen(self.link)
            # soup = BeautifulSoup(url)
            # if soup.title != None:
            #     self.title = soup.title.string
            # else:
            #     self.title = url
            # self.description = soup.findAll(attrs={"name":"description"})
        super(Node, self).save(*args, **kwargs)

    def add_link(self, other, symm=True):
        link, created = Link.objects.get_or_create(
            from_node=self,
            to_node=other)
        if symm:
            # avoid recursion by passing `symm=False`
            other.add_link(self, False)
        return link

    def remove_link(self, other, symm=True):
        Link.objects.filter(
            from_node=self,
            to_node=other).delete()
        if symm:
            # avoid recursion by passing `symm=False`
            other.remove_link(self, False)

    def get_links(self):
        return self.links.filter(
            to_links__from_other=self)

class Link(models.Model):
    from_node = models.ForeignKey(Node, related_name="from")
    to_node = models.ForeignKey(Node, related_name="to")

    def __unicode__( self ):
		return str(self.from_node) + ' - ' + str(self.to_node)

class Path(models.Model):

    title = models.CharField(max_length=200, blank=True, null=True)
    nodes = models.ManyToManyField(Node, related_name="nodes",through='PathNodeRelationship')

    def __unicode__( self ):
        if self.title:
            return self.title
        elif self.nodes:
            size = self.nodes.count()
            nodes = self.nodes.all()
            return "%s - %s (%d)"%(nodes[0],nodes[nodes.count()],size)
        else:
            return "No nodes"

    def save(self, *args, **kwargs):
        super(Path, self).save(*args, **kwargs)

        #save all not-existent links on this path
        previous_node = None
        for node in self.nodes.all():
            if previous_node is not None:
                previous_node.add_link(node)
            previous_node = node
        super(Path, self).save(*args, **kwargs)

    def create_links(sender, instance, created, **kwargs):
        if instance and created:
            previous_node = None
            for node in instance.nodes.all():
                if previous_node is not None:
                    previous_node.add_link(node)
                previous_node = node

    post_save.connect(create_links, sender="Path")

class PathNodeRelationship(models.Model):
    node = models.ForeignKey(Node)
    path = models.ForeignKey(Path)
    order_index = models.IntegerField()

    def __unicode__(self):
        return str(self.node) + " - " + str(self.order_index)

class Vector(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

""" custom method using https://docs.djangoproject.com/en/1.7/howto/custom-model-fields/ """
class VectorField(models.Field):
    description = "A Vector3"

    def __init__(self, *args, **kwargs):
        # kwargs['max_length'] = 104
        super(VectorField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(VectorField, self).deconstruct()
       # del kwargs["max_length"]
        return name, path, args, kwargs