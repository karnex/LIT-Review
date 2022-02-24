from django import forms


class TicketForm(forms.Form):
    ticket_title = forms.CharField(max_length=255, label='Titre', label_suffix='',
                                   widget=forms.TextInput(attrs={'class': 'form-control mt-2 mb-3'}))
    description = forms.CharField(label='Description', label_suffix='', required=False,
                                  widget=forms.Textarea(attrs={'class': 'form-control mt-1 mb-3'}))
    image = forms.FileField(label='image', label_suffix='', required=False,
                            widget=forms.FileInput(attrs={'class': 'form-control mt-1 mb-3'}))


class ReviewForm(forms.Form):
    review_title = forms.CharField(max_length=255, label='Titre', label_suffix='',
                                   widget=forms.TextInput(attrs={'class': 'form-control mt-2 mb-3'}))
    rating = forms.ChoiceField(label='Note', label_suffix='',
                               widget=forms.RadioSelect(attrs={'class': 'block mt-1 mb-3'}),
                               choices=[('0', ' - 0'), ('1', ' - 1'), ('2', ' - 2'), ('3', ' - 3'),
                                        ('4', ' - 4'), ('5', ' - 5')])
    comment = forms.CharField(label='Commentaire', label_suffix='',
                              widget=forms.Textarea(attrs={'class': 'form-control mt-1 mb-3'}))
