from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django import forms
from contact.models import Contact


# criando formulário
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        
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


# Create your views here
def create(request):

    if request.method == 'POST':

        context = {
            'form': ContactForm(request.POST)
        }
        return render(
            request,
            'contact/create.html',
            context,
        )

    context = {
        'form': ContactForm()
    }
    return render(
            request,
            'contact/create.html',
            context,
    )
