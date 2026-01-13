from django import forms
from .models import Dataset, Notebook


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'file']


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['dataset', 'name', 'file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.ipynb'):
            raise forms.ValidationError('Solo se permiten archivos .ipynb')
        return file
