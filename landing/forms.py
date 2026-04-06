from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'
        labels = {
            'username': 'Name',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Message',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter a subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your message here'}),
        }