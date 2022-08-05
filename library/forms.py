from django.forms import ModelForm
from .models import *

class EbookForm(ModelForm):
    class Meta:
        model=Ebook
        fields='__all__'