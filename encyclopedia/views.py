from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
import django as dj

import random

from . import util, forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    results = []
    query = request.GET.get('q')
    entries = util.list_entries()
    if query in entries:
        return get_page(request, query)

    for entry in entries:
        if query in entry:
            results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results,
    })

def get_page(request, entry):
    content = util.get_entry(entry)
    if content:
        return render(request, "encyclopedia/page.html", {
            "entry": entry, 
            "content": util.convert_to_html(content),
        })
    return HttpResponseNotFound("Page not found")

def get_random_page(request):
    randomEntry = random.choice(util.list_entries())
    return get_page(request, randomEntry)

def create_page(request):
    if request.method == "POST":
        form = forms.PageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title):
                util.save_entry(title, f'# {title}\n\n{content}')
                return HttpResponseRedirect(reverse('getPage', args=(title,)))    
            else:
                messages.error(request, "Page already exists!")
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    })
        else:
            return render(request, "encyclopedia/create.html", {
                    "form": form,
                    })

    return render(request, "encyclopedia/create.html", {
        "form": forms.PageForm(),
    })

def edit_page(request, entry):
    content = util.get_entry(entry)
    if content:
        # https://docs.djangoproject.com/en/3.2/ref/forms/api/#dynamic-initial-values
        data = {'title': entry, 'content': content}
        if request.method == "GET":
            form = forms.PageForm(data)
            form.fields['title'].widget = dj.forms.TextInput(attrs={'hidden': 'true'})
            form.fields['title'].label = ''
            return render(request, "encyclopedia/edit.html", {
                "entry": entry,
                "form": form,
                })
        if request.method == "POST":
            form = forms.PageForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"]
                util.save_entry(entry, content)
                return HttpResponseRedirect(reverse('getPage', args=(entry,)))

    return HttpResponseRedirect(reverse('index'))
