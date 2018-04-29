from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('archives/', views.ArchivesView.as_view(), name='archives'),
    path('create/', views.LinkCreateView.as_view(), name='create'),
    path('<int:link_id>/edit/', views.LinkUpdateView.as_view(), name='edit'),
    path('<int:link_id>/archive/', views.LinkArchiveView, name='archive'),
    path('<int:link_id>/delete/', views.LinkDeleteView.as_view(), name='delete')
]
