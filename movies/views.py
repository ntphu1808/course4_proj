# Create your views here.

import urllib.parse

from celery.exceptions import TimeoutError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from course4_proj.celery import app
from movies.models import Movie
from movies.tasks import search_and_save


def search(request):
    search_term = request.GET["search_term"] #retrieves the search term
    res = search_and_save.delay(search_term)
    try:
        res.get(timeout=2) #wait two seconds for a result
    except TimeoutError: #if none is received after 2 secs
        return redirect( #then redirects to waiting view
            reverse("search_wait", args=(res.id,)) # res.id is the id of the task
            + "?search_term="
            + urllib.parse.quote_plus(search_term)
        )
    return redirect( # if there are results
        reverse("search_results")   #redirect to search_result view
        + "?search_term="
        + urllib.parse.quote_plus(search_term),
        permanent=False,
    )

def search_wait(request, result_uuid): #result_uuid is the task uuid
    search_term = request.GET["search_term"]
    res = app.AsyncResult(result_uuid)

    try:
        res.get(timeout=-1) #timeout = 0 means waiting forever, -1 means get result immediately.
    except TimeoutError: 
        return HttpResponse("Task pending, please refresh.", status=200)

    return redirect(  
        reverse("search_results")
        + "?search_term="
        + urllib.parse.quote_plus(search_term)
    )

def search_results(request): # querying the database for search term and returning all the results as plain text list.
    search_term = request.GET["search_term"]
    movies = Movie.objects.filter(title__icontains=search_term)
    return HttpResponse(
        "\n".join([movie.title for movie in movies]), content_type="text/plain"
    )