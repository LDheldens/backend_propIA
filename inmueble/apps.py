from django.apps import AppConfig



class InmuebleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inmueble'

    def ready(self):
        import inmueble.signals