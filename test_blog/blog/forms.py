from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['header', 'text']
        labels = {
            'header': _('Header'),
            'text': _('Text'),
        }
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
