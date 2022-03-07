from django.db import models

# Create your models here.

class SearchTerm(models.Model): #model for search term.
    class Meta:
        ordering = ["id"]

    term = models.TextField(unique=True) #term is unique
    last_search = models.DateTimeField(auto_now=True) #store the date right the time the search term is added

class Genre(models.Model): 
    class Meta:
        ordering = ["name"]

    name = models.TextField(unique=True) #name for Genre is unique

class Movie(models.Model):
    class Meta:
        ordering = ["title", "year"]

    title = models.TextField()
    year = models.PositiveIntegerField()
    runtime_minutes = models.PositiveIntegerField(null=True)
    
    #imdb id is unique and we're treat this as a primary key
    # It will also allow us to create a mapping between the record in our local DB and the data provided by OMDb
    imdb_id = models.SlugField(unique=True) 
    
    genres = models.ManyToManyField(Genre, related_name="movies")
    plot = models.TextField(null=True, blank=True)
    is_full_record = models.BooleanField(default=False)