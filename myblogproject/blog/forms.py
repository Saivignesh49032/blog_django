# blog/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # FIX: Only include the 'body' field
        fields = ('body',) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({
            'placeholder': 'Add a comment...',
            'rows': 2
        })