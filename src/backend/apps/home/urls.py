# -*- coding: utf-8 -*-
from allauth.account.views import logout as allauth_logout
from allauth.socialaccount.providers.edx.urls import (
    urlpatterns as allauth_edx_urlpatterns,
)
from apps.home import views
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic.base import RedirectView

app_name = 'home'

favicon_view = RedirectView.as_view(
    url="/static/assets/img/favicon.ico", permanent=True
)

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("error-500", views.error_500, name="error-500"),
    # Firefox still sends requests to /favicon.ico
    re_path(r"^favicon\.ico$", favicon_view),
]

allauth_edx_urlpatterns += [
    path("logout/", allauth_logout, name="account_logout"),
]
urlpatterns += [
    path("accounts/", include(allauth_edx_urlpatterns)),
]
