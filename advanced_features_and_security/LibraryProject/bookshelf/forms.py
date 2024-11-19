from django import forms

class ExampleForm(forms.ModelForm):
    class Meta:
        model = book
        fields = ['title', 'author', 'description']
