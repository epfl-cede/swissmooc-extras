# -*- coding: utf-8 -*-
from apps.split_logs.views import APICourseDetails
from apps.split_logs.views import APICoursesList
from apps.split_logs.views import APIOrganisationsList
from apps.split_logs.views import CourseDetails
from apps.split_logs.views import IndexView
from apps.split_logs.views import OrganisationDetails
from django.urls import path
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'split-logs'

urlpatterns = [
    path(
        "api/organisations/",
        APIOrganisationsList.as_view({"get": "list"}),
        name="split_logs",
    ),
    path(
        "api/courses/<int:organisation_id>/",
        APICoursesList.as_view({"get": "list"})
    ),
    path(
        "api/course/<int:pk>/",
        APICourseDetails.as_view({"get": "retrieve"})
    ),
    path(
        "api/course/<str:course_id>/",
        APICourseDetails.as_view({"get": "retrieve"})
    ),
    path(
        "organisation/<int:pk>/",
        OrganisationDetails.as_view(),
        name="organisation"
    ),
    path(
        "course/<int:pk>/<str:unit_id>/",
        CourseDetails.as_view(),
        name="unit"
    ),
    path(
        "ccourse/<int:pk>/",
        CourseDetails.as_view(),
        name="course"
    ),
    re_path(r"^.*", IndexView.as_view(), name="index")
]

urlpatterns = format_suffix_patterns(urlpatterns)
