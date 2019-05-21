from django.conf.urls import url
from . import views

urlpatterns = [
# render this result of this views API view, and return it to the screen
    url(r'^hello-view/', views.HelloApiView.as_view()),
]
