from hashlib import md5

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
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


class PostOnlyMixin:
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('index')


class LinkPostMixin(LoginRequiredMixin, PostOnlyMixin):
    model = Link
    pk_url_kwarg = 'link_id'


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


class LinkCreateView(LinkPostMixin, CreateView):
    fields = ['url', 'title', 'description', 'category']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        return super(LinkCreateView, self).form_valid(form)


class LinkUpdateView(LinkPostMixin, UpdateView):
    pass


class LinkArchiveView(LinkPostMixin, UpdateView):
    pass


class LinkDeleteView(LinkPostMixin, PostOnlyMixin, DeleteView):
    pass
