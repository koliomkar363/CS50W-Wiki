import markdown2
from django.shortcuts import render
from random import choice
from . import util
from .forms import NewEntryForm, SearchForm, EditEntryForm


def index(request):

    # Get the entries from the list_entries function of util.py
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": SearchForm()
    })


def url_search(request, title):

    # Get the title from the get_entry function of util.py
    entry_title = util.get_entry(title)

    # If the entry doesn't exist, redirect to the error page
    if entry_title is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "search": SearchForm()
        })

    # Else redirect to the desired entry page
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry_title),
            "search": SearchForm()
        })


def entry_search(request):

    # POST Method: Display the search result(s)
    if request.method == "POST":
        results = []
        # Populate the SearchForm
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['search_entry'].lower()
            entries = util.list_entries()

            for entry in entries:

                # Display the entry page if an exact match is found
                if query == entry.lower():
                    return url_search(request, query)

                # Populate the result's list with the entries having the matched substring
                elif query in entry.lower():
                    results.append(entry)

            # Total no of entries with the given substring
            num = len(results)

            # Display a list of entries which have the required substring
            return render(request, "encyclopedia/search.html", {
                "search": SearchForm(request.POST),
                "results": results,
                "num": num,
                "query": form.cleaned_data['search_entry']
            })

    # GET Method: Redirects to the search.html
    else:
        return render(request, "encyclopedia/search.html", {
            "search": SearchForm()
        })


def create(request):

    # POST Method: Creates a new entry
    if request.method == "POST":
        # Populate the NewEntryForm
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            entries = util.list_entries()

            # Check if the desired title is available
            if title in entries:
                err = "Title already exists! Please provide a new title!"

                # If title is already taken, it throws an error
                return render(request, "encyclopedia/create.html", {
                    "form": NewEntryForm(),
                    "search": SearchForm(),
                    "error": err
                })

            # If title is available, save it with save_entry function
            else:
                new_title = '# ' + title + '\n'
                new_body = body
                new_content = new_title + new_body
                util.save_entry(title, new_content)

                # Redirects to the saved title page
                return url_search(request, title)

    # GET Method: Redirects to the create.html
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm(),
            "search": SearchForm()
        })


def edit_entry(request, title):

    # POST Method: Pre-populates the text-area with the existing content
    if request.method == "POST":
        entry = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": EditEntryForm(initial={'content': entry}),
            "search": SearchForm(),
        })


def submit_entry(request, title):

    # POST Method: Redirects to the saved entry's url_search function
    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)

            return url_search(request, title)


def random(request):

    # Display a random page from the list of entries
    return url_search(request, choice(util.list_entries()))
