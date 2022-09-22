from django import forms


RADIO_CHOICES= [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ]

class UserForm(forms.Form):
    # first_name = forms.CharField(required=True, max_length=100)
    radio_button = forms.CharField(label='What is your rating?', widget=forms.RadioSelect(choices=RADIO_CHOICES), required=True)

    def __str__(self):
        return self.radio_button
