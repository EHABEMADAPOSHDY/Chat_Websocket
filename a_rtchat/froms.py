from django import forms
from django.forms import ModelForm

from .models import *


class ChatmessageCreateForm(ModelForm):

    class Meta:
        model = GroupMessage
        fields = ['body']

        widgets = {
            'body': forms.TextInput(
                attrs={
                    'placeholder': 'Add message ...',
                    'class': 'p-4 text-black',
                    'maxlength': '300',
                    'autofocus': True,
                }
            ),
        }