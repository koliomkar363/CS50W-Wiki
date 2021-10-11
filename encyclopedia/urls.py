from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.url_search, name="title"),
    path("search/", views.entry_search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:title>", views.edit_entry, name="edit"),
    path("edit/<str:title>/submit", views.submit_entry, name="submit"),
    path("random/", views.random, name="random")
]
