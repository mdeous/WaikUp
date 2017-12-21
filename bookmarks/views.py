from hashlib import md5

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET

from .models import Link


def global_context(request):
    context = {}
    if request.user.is_authenticated:
        email_hash = md5(request.user.email.encode('utf-8')).hexdigest()
        context['gravatar'] = 'https://www.gravatar.com/avatar/{}?d=mm'.format(email_hash)
    else:
        context['gravatar'] = 'https://www.gravatar.com/avatar/?d=mm'
    return context


@login_required
@require_GET
def link_list(request):
    try:
        archived = bool(int(request.GET.get('archived', 0)))
    except ValueError:
        archived = False
    current_page = 'link-list'
    if archived:
        current_page = 'archives'
    links = Link.objects.filter(archived=archived)
    return render(request, 'link_list.html', context={'link_list': links, 'current_page': current_page})


@login_required
@require_POST
def link_create(request):
    return HttpResponse('Link created')


@login_required
@require_POST
def link_edit(request, link_id):
    return HttpResponse('Link {} edited'.format(link_id))


@login_required
@require_POST
def link_toggle_archive(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    link.archived = not link.archived
    link.save()
    messages.add_message(request, messages.SUCCESS, 'Link {} {}archived'.format(
        link_id,
        '' if link.archived else 'un'
    ))
    return redirect('link-list')


@login_required
@require_POST
def link_delete(request, link_id):
    return HttpResponse('Link {} deleted'.format(link_id))
