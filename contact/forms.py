from django import forms
from django.core.exceptions import ValidationError
from contact.models import Contact


# criando formulário
class ContactForm(forms.ModelForm):

    # usando WIDGETS
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'classe-a classe-b',
                'placeholder': 'type here'
            }
        ),
        # label='Mudar o nome da label do campo'
        help_text='Type contact first name'  # Renderizar no template 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Outro modo de utilizar WIDGETS (tem de ter o __init__)
        # self.fields['first_name'].widget.attrs.update({
        #     'class': 'classe-a classe-b',
        #     'placeholder': 'type here'
        # })

    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
        )
        
        # Usando WIDGETS de outro modo sem o __init__
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'class': 'classe-a classe-b',
        #             'placeholder': 'type here'
        #         }
        #     )
        # }

    def clean(self):
        # cleaned_data = self.cleaned_data

        self.add_error(
            None,
            ValidationError(
                'Mensagem de erro',
                code='invalid'
            )
        )

        self.add_error(
            None,
            ValidationError(
                'Mensagem de erro 2',
                code='invalid'
            )
        )
        return super().clean()
