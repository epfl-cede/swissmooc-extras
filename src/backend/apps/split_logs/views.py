# -*- coding: utf-8 -*-
import logging

from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from apps.split_logs.serializers import CourseListSerializer
from apps.split_logs.serializers import CourseSerializer
from apps.split_logs.serializers import OrganisationSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

logger = logging.getLogger(__name__)


class OrganisationsList(ReadOnlyModelViewSet):
    queryset = Organisation.objects.filter(active=True)
    serializer_class = OrganisationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CoursesList(ReadOnlyModelViewSet):
    lookup_organisation_id_kwarg = "organisation_id"
    serializer_class = CourseListSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation_id = self.kwargs.get(self.lookup_organisation_id_kwarg)
        courses = Course.objects.filter(active=True, organisation_id=organisation_id)
        return courses


class CourseDetails(ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None, course_id=None):
        queryset = Course.objects.all()
        if pk:
            course = get_object_or_404(queryset, pk=pk)
        else:
            course = get_object_or_404(queryset, course_id=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
