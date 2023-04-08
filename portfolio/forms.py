from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = ("user_name", "user_email", "comment_text",)
        exclude = ["project"]
        labels = {
            "user_name": "Your Name",
            "user_email": "Your Email",
            "comment_text": "Comment text"
        }
        widgets = {
            "user_name": forms.TextInput(attrs={'placeholder': ' '}),
            "user_email": forms.TextInput(attrs={'placeholder': ' '}),
            "comment_text": forms.Textarea(attrs={'placeholder': ' '})
        }
