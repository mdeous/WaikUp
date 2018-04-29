from hashlib import md5

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from .forms import NewLinkForm
from .models import Link


def global_context(request):
    context = {}
    if request.user.is_authenticated:
        email_hash = md5(request.user.email.encode('utf-8')).hexdigest()
        context['gravatar'] = 'https://www.gravatar.com/avatar/{}?d=mm'.format(email_hash)
    else:
        context['gravatar'] = 'https://www.gravatar.com/avatar/?d=mm'
    context['new_link_form'] = NewLinkForm()
    return context


class LinkListView(LoginRequiredMixin, ListView):
    template_name = 'link_list.html'
    model = Link
    current_page = ''

    def get_queryset(self):
        queryset = self.model.objects.filter(archived=self.current_page == 'archives').all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(LinkListView, self).get_context_data(*args, **kwargs)
        context['current_page'] = self.current_page
        return context


class IndexView(LinkListView):
    current_page = 'link_list'


class ArchivesView(LinkListView):
    current_page = 'archives'


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link


class LinkUpdateView(LoginRequiredMixin, UpdateView):
    model = Link
    pk_url_kwarg = 'link_id'


class LinkArchiveView(LoginRequiredMixin, UpdateView):
    model = Link
    pk_url_kwarg = 'link_id'


class LinkDeleteView(LoginRequiredMixin, DeleteView):
    model = Link
    pk_url_kwarg = 'link_id'
