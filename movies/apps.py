from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    #notice, the comment # noqa has to be there so this ready method would work correctly
    def ready(self):
        import movies.signals  # noqa
