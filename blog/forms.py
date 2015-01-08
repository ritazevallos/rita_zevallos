from ritazevallos.blog.models import Path, Node
from django import forms
from django.forms.models import modelformset_factory

NodeFormset = modelformset_factory(Node, extra=1)

class PathForm(forms.ModelForm):
	class Meta:
		model = Path
        exclude = ('nodes')
	nodes = forms.ModelMultipleChoiceField(
	    queryset=Node.objects.all().order_by('-updated_at','-date'),
							widget=forms.CheckboxSelectMultiple(),
	    )

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ('title',
        'link',
        'img',
        'text',
        'private')
