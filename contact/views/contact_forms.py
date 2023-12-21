from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from contact.forms import ContactForm
from contact.models import Contact


# Create your views here

@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            # assim não commita a BD de imediato
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.show = True
            contact.save()
            # permite fazer algo antes de commitar na BD
            # exemplo:
            # contact.show = False
            # contact.save()    -- Agora faz o commit na BD

            # depois de commitar redireciona a página
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context,
        )

    context = {
        'form': ContactForm(),
        'form_action': form_action,
    }
    return render(
            request,
            'contact/create.html',
            context,
    )


@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True,
        owner=request.user,
    )

    form_action = reverse('contact:update', args=(contact_id,))

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            form.save()
            # contact = form.save
            # depois de commitar redireciona a página
            return redirect('contact:update', contact_id=contact.pk)

        return render(
            request,
            'contact/create.html',
            context,
        )

    context = {
        'form': ContactForm(instance=contact),
        'form_action': form_action,
    }
    return render(
            request,
            'contact/create.html',
            context,
    )


@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(
        Contact,
        pk=contact_id,
        show=True,
        owner=request.user,
    )

    confirmation = request.POST.get('confirmation', 'no')
    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )
