from django import forms


class SearchForm(forms.Form):
    Word = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Enter a word', 'class': 'input'}))


class IndexForm(forms.Form):
    Text = forms.CharField(required=True,
                           widget=forms.Textarea(attrs={'rows': 20, 'cols': 100, 'placeholder': 'Enter text'}))

