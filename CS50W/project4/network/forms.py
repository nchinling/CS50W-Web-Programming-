from django import forms

class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)