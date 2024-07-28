import logging
from django.apps import AppConfig
import seqlog

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.setup.mediator_setup import register_handlers
        register_handlers()
        seqlog.log_to_seq(
            server_url="http://localhost:5342/",
            api_key=None,
            level=logging.INFO,
            batch_size=10,
            auto_flush_timeout=10,  # seconds
            override_root_logger=True,
        )
