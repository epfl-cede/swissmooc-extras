# -*- coding: utf-8 -*-
import logging

from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from apps.split_logs.serializers import CourseSerializer
from apps.split_logs.serializers import OrganisationSerializer
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
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    # permission_classes = [permissions.IsAuthenticated]
