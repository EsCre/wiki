from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import random
from . import util
import markdown2

class SearchForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewContent(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        'placeholder': 'Enter the title of the article',
        'class':'form-control',
        'id':'exampleFormControlInput1'
    }))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        'placeholder': 'Enter the article',
        'class': 'form-control',
        'id': 'exampleFormControlTextarea1',
        'rows':'3'
    }))

class EditContent(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={
        'placeholder': 'Enter the title of the article',
        'class':'form-control',
        'id':'exampleFormControlInput1',
        'readonly':'readonly'
    }))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
        'placeholder': 'Enter the article',
        'class': 'form-control',
        'id': 'exampleFormControlTextarea1',
        'rows':'3'
    }))

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if search.lower() in util.lower_casing(util.list_entries()):
                return HttpResponseRedirect(reverse("wiki:entry_page", args=[search]))

            result = util.Filter(util.list_entries(), [search])
            return render(request, "encyclopedia/index.html", {
                "title": "Searched Results",
                "entries": result,
                "method": request.method,
                "form": SearchForm(),
            })
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries(),
        "form":SearchForm(),
        "random_entry":random.choice(util.list_entries())
    })

def entry_page(request, entry):
    if entry == "creating":
        if request.method == "POST":
            form_content = NewContent(request.POST)
            if form_content.is_valid():
                title = form_content.cleaned_data["title"]
                content = form_content.cleaned_data["content"]
                if title.lower() in util.lower_casing(util.list_entries()):
                    return render(request, "encyclopedia/error_page.html")
                else:
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("wiki:entry_page", args=[title]))
        else:
            return render(request, "encyclopedia/content_creator.html", {
                "form_content": NewContent(),
                "random_entry": random.choice(util.list_entries())
            })
    else:
        return render(request, "encyclopedia/entry_page.html", {
            "entry": entry,
            "content": markdown2.markdown(util.get_entry(entry)),
            "random_entry": random.choice(util.list_entries())
        })

def editor(request, entry):
    arr1 = entry.split("/")
    if request.method == "POST":
        form_edited = EditContent(request.POST)
        if form_edited.is_valid():
            title = form_edited.cleaned_data["title"]
            content = form_edited.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry_page", args=[title]))
    return render(request, "encyclopedia/editor.html", {
        'title':arr1[0],
        "formEdit":EditContent(initial={'title':arr1[0] ,'content': util.get_entry(arr1[0])}),
        "random_entry": random.choice(util.list_entries())
    })
