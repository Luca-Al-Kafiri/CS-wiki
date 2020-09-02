from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entries = util.list_entries()
    if entry not in entries:
        return render(request, "encyclopedia/entry.html",{'entry':entry, 'message':'Page not found'})
    post = util.get_entry(entry)
    content = markdown(post)
    return render(request, "encyclopedia/entry.html",{"content":content, 'entry':entry})

def search(request):
    q = request.GET.get('q')
    entries = util.list_entries()
    results = []
    if q in entries:
        return redirect('entry', entry=q)
    for i in entries:
        if q.lower() in i.lower():
            results.append(i)
    return render(request, 'encyclopedia/search.html',{'results':results, 'q':q})

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        entries = util.list_entries()
        if title in entries:
            return render(request, 'encyclopedia/create.html', {'message':'Page already exist'})
        util.save_entry(title, content)
        return redirect('entry', entry=title)
    return render(request, 'encyclopedia/create.html')

def edit(request, entry):
    if request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(entry, content)
        return redirect('entry', entry=entry)
    else:
        content = util.get_entry(entry)
        return render(request, 'encyclopedia/edit.html',{'entry': entry, 'content':content})

def random_page(request):
    entries = util.list_entries()
    x = random.randint(1, len(entries)-1)
    entry = entries[x]
    return redirect('entry', entry=entry)