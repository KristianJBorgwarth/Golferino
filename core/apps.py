from django.apps import AppConfig



class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.setup.mediator_setup import register_handlers
        register_handlers()

        from django.contrib.auth.models import User
        from django.db import models
        User.add_to_class('is_verified', models.BooleanField(default=False))
