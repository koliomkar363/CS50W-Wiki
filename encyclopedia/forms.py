from django import forms


class SearchForm(forms.Form):
    search_entry = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Search Encyclopedia'
        }
    ))


class NewEntryForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'New Title'
        }
    ))

    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'placeholder': 'Markdown Content',
            'style': 'height:300px'
        }
    ))


class EditEntryForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'placeholder': 'Markdown Content',
            'style': 'height:300px'
        }
    ))
