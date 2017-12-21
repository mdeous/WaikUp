from django.urls import path

from . import views


urlpatterns = [
    path('', views.link_list, name='link-list'),
    path('create/', views.link_create, name='link-create'),
    path('<int:link_id>/edit/', views.link_edit, name='link-edit'),
    path('<int:link_id>/archive/', views.link_toggle_archive, name='link-toggle-archive'),
    path('<int:link_id>/delete/', views.link_delete, name='link-delete')
]
