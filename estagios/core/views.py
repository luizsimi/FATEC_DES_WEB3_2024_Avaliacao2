from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from core.models import VagaModel
from core.forms import VagaForm

def index(request):
    if request.method == 'GET':
        return render(request, "index.html")
    return HttpResponseRedirect(reverse('core:index'))

def create(request):
    if request.method == 'POST':
        form = VagaForm(request.POST)
        if form.is_valid():
            VagaModel.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse('core:index'))
        contexto = {'form': form}
        return render(request, "cadastro.html", contexto)
    contexto = {'form': VagaForm()}
    return render(request, 'cadastro.html', contexto)

def read(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        try:
            vaga = VagaModel.objects.get(pk=id)
            contexto = {'vaga': vaga}
        except ValueError:
            contexto = {}
        return render(request, "detalhes.html", contexto)
    contexto = {'vagas': VagaModel.objects.all()}
    return render(request, 'listar.html', contexto)

def update(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        try:
            form = VagaForm(VagaModel.objects.get(pk=id).__dict__)
            contexto = {'form': form, 'pk':id}
        except ValueError:
            contexto = {}
        return render(request, "atualizar2.html", contexto)
    contexto = {'vagas': VagaModel.objects.all()}
    return render(request, 'atualizar.html', contexto)

def confirm_update(request):
    if request.method == 'POST':
        id = request.POST['id']
        instance = get_object_or_404(VagaModel, id=id)
        form = VagaForm(request.POST)
        if form.is_valid():
            instance.__dict__.update(**form.cleaned_data)
            instance.save()
            contexto = {'vagas': VagaModel.objects.all()}
            return render(request, 'atualizar.html', contexto)
        contexto = {'form': form, 'pk':id}
        return render(request, "atualizar2.html", contexto)
    return render(request, "index.html")

def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        try:
            VagaModel.objects.get(pk=id).delete()
        except:
            pass
        return render(request, "index.html")
    contexto = {'vagas': VagaModel.objects.all()}
    return render(request, 'remover.html', contexto)
