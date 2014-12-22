from django.db import models
from django.db.models.signals import post_save

class Tag(models.Model):
	name = models.CharField(max_length=200, null=False)

	def __unicode__( self ):
		return self.name

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
    locationX = models.IntegerField(blank=True, null=True)
    locationY = models.IntegerField(blank=True, null=True)
    locationZ = models.IntegerField(blank=True, null=True)

    def __unicode__( self ):
        return self.title

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
		return self.from_node.title + ' - ' + self.to_node.title

class Path(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    nodes = models.ManyToManyField(Node, related_name="nodes",through='PathNodeRelationship')

    def __unicode__( self ):
        nodes = self.nodes.all()
        return nodes[0].title + " - " + nodes[len(nodes)-1].title

    def save(self, *args, **kwargs):
        super(Path, self).save(*args, **kwargs)

        # save all not-existent links on this path
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
        return self.node.title + " - " + str(self.order_index)