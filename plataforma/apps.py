from django.apps import AppConfig


class PlataformaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plataforma'
    verbose_name = 'Plataforma Administrativa'

    def ready(self):
        """Importar signals cuando la app esté lista"""
        import plataforma.signals