from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from contact.models import Contact


# criando formulário
class ContactForm(forms.ModelForm):

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False,
    )
    
    # usando WIDGETS
    first_name = forms.CharField(
         widget=forms.TextInput(
             attrs={
                 'autofocus': '',
             }
         ),
    #     # label='Mudar o nome da label do campo'
    #     # help_text='Type contact first name'  # Renderizar no template
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

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
            'phone', 'email',
            'description', 'category',
            'picture',
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
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'First and last names are the same!',
                code='invalid',
            )
            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        # validando um campo especifico do formulário
        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'Não digite ABC neste campo',
                    code='invalid'
                )
            )
        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('This e-mail already exists', code='invalid')
            )

        return email


class RegisterUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more then 2 letters'
        },
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more then 2 letters'
        },
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label='Password 2',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='The specified passwords must be identical',
        required=False,
    )

    class Meta():
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Passwords do not match.')
                )
        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:

            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('This e-mail already exists', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )
        return password1

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)

        password = cleaned_data.get('password1')
        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user
