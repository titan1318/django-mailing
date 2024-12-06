from django.forms import ModelForm, BooleanField

from blog.models import Post


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-class'


class PostForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Post
        exclude = ['number_of_views']