from django.shortcuts import render, redirect, get_object_or_404
from .models import Dataset, Notebook
from .forms import DatasetForm, NotebookForm

import nbformat
from nbconvert import HTMLExporter
from traitlets.config import Config  
from django.utils.safestring import mark_safe
import os # Necesario para eliminar archivos físicos

def dashboard(request):
    datasets = Dataset.objects.all().order_by('-uploaded_at')
    notebooks = Notebook.objects.all().order_by('-uploaded_at')

    dataset_form = DatasetForm()
    notebook_form = NotebookForm()

    if request.method == 'POST':
        if 'upload_dataset' in request.POST:
            dataset_form = DatasetForm(request.POST, request.FILES)
            if dataset_form.is_valid():
                dataset_form.save()
                return redirect('dashboard')

        elif 'upload_notebook' in request.POST:
            notebook_form = NotebookForm(request.POST, request.FILES)
            if notebook_form.is_valid():
                notebook_form.save()
                return redirect('dashboard')

    return render(request, 'core/dashboard.html', {
        'datasets': datasets,
        'notebooks': notebooks,
        'dataset_form': dataset_form,
        'notebook_form': notebook_form
    })

def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    return render(request, 'core/dataset_detail.html', {
        'dataset': dataset
    })

def notebook_detail(request, notebook_id):
    notebook = get_object_or_404(Notebook, id=notebook_id)

    # Validación de seguridad para que no truene si el archivo no está
    if not os.path.exists(notebook.file.path):
        return render(request, 'core/notebook_detail.html', {
            'notebook': notebook,
            'notebook_html': mark_safe(f"<div class='alert alert-danger'>Error: El archivo físico no existe. Ruta buscada: {notebook.file.path}</div>")
        })

    with open(notebook.file.path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    c = Config()
    c.HTMLExporter.exclude_input_prompt = True
    c.HTMLExporter.exclude_output_prompt = True
    
    exporter = HTMLExporter(config=c)
    exporter.exclude_input = False  
    
    body, _ = exporter.from_notebook_node(nb)

    return render(request, 'core/notebook_detail.html', {
        'notebook': notebook,
        'notebook_html': mark_safe(body)
    })

# NUEVA FUNCIÓN DE ELIMINACIÓN
def delete_notebook(request, notebook_id):
    notebook = get_object_or_404(Notebook, id=notebook_id)
    if request.method == 'POST':
        # Borra el archivo físico si existe
        if notebook.file and os.path.exists(notebook.file.path):
            os.remove(notebook.file.path)
        # Borra el registro de la DB
        notebook.delete()
    return redirect('dashboard')