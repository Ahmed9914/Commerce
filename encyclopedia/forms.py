from django import forms


class PageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter page title', 'class': 'form-control my-2 w-50'}),
                            label='Page Title',
                            strip=True)
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter content in markdown format',
                                                           'class': 'form-control w-75 my-2',}),
                                                           label='Page Content')
