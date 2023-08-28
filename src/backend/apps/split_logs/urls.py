# -*- coding: utf-8 -*-
from apps.split_logs.views import CoursesList
from apps.split_logs.views import OrganisationsList
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("api/organisations/", OrganisationsList.as_view({"get": "list"})),
    path("api/courses/",       CoursesList.as_view({"get": "list"})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
