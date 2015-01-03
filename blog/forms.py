from ritazevallos.blog.models import Path, Node
from django import forms
from django.forms.models import modelformset_factory

NodeFormset = modelformset_factory(Node, extra=1)

class PathForm(forms.ModelForm):
	class Meta:
		model = Path
        exclude = ('nodes',)

	nodes = forms.ModelMultipleChoiceField(
	    queryset=Node.objects.all(),
							widget=forms.CheckboxSelectMultiple(),
	    )

