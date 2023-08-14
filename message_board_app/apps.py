from django.apps import AppConfig


class MessageBoardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message_board_app'

    def ready(self):
        import message_board_app.signals


