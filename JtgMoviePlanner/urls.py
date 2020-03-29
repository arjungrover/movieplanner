"""JtgMoviePlanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

from user.views import SignupViewSet, LoginView, EmailVerify, GetUserView
from movie.views import MovieViewSet, MovieShowViewSet, GetAllMovies, GetAllShows

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^verify/', EmailVerify.as_view(), name="verify"),
    url(r'^get-movies', GetAllMovies.as_view(), name="getmovies"),
    url(r'^get-shows', GetAllShows.as_view(), name="getshows"),
    url(r'^get-user', GetUserView.as_view(), name="getuser"),
]

router = routers.SimpleRouter()
router.register(r'signup', SignupViewSet, basename="signup")
urlpatterns = urlpatterns + router.urls
router.register(r'add-movies', MovieViewSet, basename="addmovies")
urlpatterns = urlpatterns + router.urls
router.register(r'add-shows', MovieShowViewSet, basename="addshows")
urlpatterns = urlpatterns + router.urls

obtain_auth_token = LoginView.as_view()
