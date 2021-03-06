from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from . import views


# create a new var called router
router = DefaultRouter()

# register a router that points to
# our HelloViewSet
# The first para, the name of our apis that we want to call it
# The second para, the name of the viewset we want to assign to
# this router
# The third para, we need to give a base name.
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')

# No need to specify base name when registering a model viewset.
# because django rest framework can automatically figure it out
# by looking at the model that's registered with the serializer that's registered
# on our viewset
router.register('profile', views.UserProfileViewSet)
# login is the viewset but not the model viewset, so we need to ser base_name
router.register('login', views.LoginViewSet, base_name='login')
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
# render this result of this views API view, and return it to the screen
    url(r'^hello-view/', views.HelloApiView.as_view()),
# assign a new url with our router
# our router object can create a url for us
# That's why we need the include to include router.urls
# Add a blank str here is because if it can't match
# a url, then it's going to feed it basically into our
# router
    url(r'', include(router.urls))
]
