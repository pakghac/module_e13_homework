from django import forms

from message_board_app.models import Response


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = [
            'isAccepted'
        ]
