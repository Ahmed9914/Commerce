from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/create_page/", views.create_page, name="createPage"),
    path("wiki/edit_page/<str:entry>", views.edit_page, name="editPage"),
    path("wiki/<str:entry>", views.get_page, name="getPage"),
    path("wiki/random/", views.get_random_page, name="randomPage"),
]
