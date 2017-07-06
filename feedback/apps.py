from django.apps import AppConfig as DjangoAppConfig


class FeedbackConfig(DjangoAppConfig):
    name = 'feedback'

    def ready(self):
        # Import the module to cause registration of the signal
        from .signals import send_feedback_notification  # noqa
