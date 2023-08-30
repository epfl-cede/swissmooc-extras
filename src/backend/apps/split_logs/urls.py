# -*- coding: utf-8 -*-
from apps.split_logs.views import CourseDetails
from apps.split_logs.views import CoursesList
from apps.split_logs.views import OrganisationsList
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("api/organisations/", OrganisationsList.as_view({"get": "list"})),
    path("api/courses/<int:organisation_id>/", CoursesList.as_view({"get": "list"})),
    path("api/course/<int:pk>/", CourseDetails.as_view({"get": "retrieve"})),
]

urlpatterns = format_suffix_patterns(urlpatterns)
