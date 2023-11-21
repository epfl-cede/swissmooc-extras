# -*- coding: utf-8 -*-
import logging

from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from apps.split_logs.serializers import CourseListSerializer
from apps.split_logs.serializers import CourseSerializer
from apps.split_logs.serializers import OrganisationSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'split_logs/index.html'
    context_object_name = 'organisation_list'

    def get_queryset(self):
        return Organisation.objects.all()

    # if not request.user.is_authenticated:
    #     return redirect(reverse("home"))


class OrganisationDetails(DetailView):
    model = Organisation
    template_name = 'split_logs/organisation.html'


class CourseDetails(DetailView):
    model = Course
    template_name = 'split_logs/course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'unit_id' in self.kwargs:
            context['unit_id'] = self.kwargs['unit_id']
            context['tasks'] = [1, 2, 3]
        else:
            context['unit_id'] = None
            context['tasks'] = None
        return context


class APIOrganisationsList(ReadOnlyModelViewSet):
    queryset = Organisation.objects.filter(active=True)
    serializer_class = OrganisationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class APICoursesList(ReadOnlyModelViewSet):
    lookup_organisation_id_kwarg = "organisation_id"
    serializer_class = CourseListSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        organisation_id = self.kwargs.get(self.lookup_organisation_id_kwarg)
        courses = Course.objects.filter(active=True, organisation_id=organisation_id)
        return courses


class APICourseDetails(ReadOnlyModelViewSet):
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
