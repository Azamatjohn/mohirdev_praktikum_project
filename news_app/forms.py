from django import forms
from .models import Contact, Comments



class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        # fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
