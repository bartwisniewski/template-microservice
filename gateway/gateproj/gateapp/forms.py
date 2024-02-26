from django import forms


class BookForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()
    year = forms.DecimalField(max_digits=4)
