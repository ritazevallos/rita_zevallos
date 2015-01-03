from ritazevallos.because.models import Beginning, Ending
from django import forms

class BeginningForm(forms.ModelForm):
	class Meta:
		model = Beginning
	fields = ('text','lat','lng')

class EndingForm(forms.ModelForm):
	class Meta:
		model = Ending
	widgets = {'beginning': forms.HiddenInput()}
	fields = ('text','lat','lng')