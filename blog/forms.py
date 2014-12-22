from ritazevallos.blog.models import Path, Node
from django import forms

class PathForm(forms.ModelForm):
	class Meta:
		model = Path
        exclude = ('nodes',)

	nodes = forms.ModelMultipleChoiceField(
	    queryset=Node.objects.all(),
							widget=forms.CheckboxSelectMultiple(),
	    )

