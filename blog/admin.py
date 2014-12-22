from django.contrib import admin

from ritazevallos.blog.models import Tag, Node, Link, Path

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tag, TagAdmin)

class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Link, LinkAdmin)

class LinkInline(admin.StackedInline):
    model = Link
    fk_name = 'from_node'

class NodeAdmin(admin.ModelAdmin):
    inlines = [LinkInline]
admin.site.register(Node, NodeAdmin)

class NodeInline(admin.TabularInline):
    model = Path.nodes.through
    extra = 1

class PathAdmin(admin.ModelAdmin):
      inlines = (NodeInline,)
admin.site.register(Path, PathAdmin)