from django import forms
from django.core.exceptions import ValidationError
from .models import TodoList,Comment
from django.forms import DateInput

class TodoListSendForm(forms.Form):
    description = forms.CharField(max_length=25)
    name_author = forms.CharField(max_length=25)
    tasks = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    to = forms.EmailField()

class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['date', 'tasks']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')

        if TodoList.objects.filter(date=date).exists():
            self.add_error('date', "У вас уже есть список дел на данный день.")

        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','text']