from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry_page, name = "entry_page"),
    path("creating", views.entry_page, name = "content"),
    path("<str:entry>/editing", views.editor, name = "editing"),
]
