from django import forms
from django.forms import FileInput, ClearableFileInput
from django.template import loader
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class ImageWidget(ClearableFileInput):
    template_name = '_widgets/image.html'
    
    def render(self, name, value, attrs=None, renderer=None):
        return super(ImageWidget, self).render(name, value, attrs, renderer)
