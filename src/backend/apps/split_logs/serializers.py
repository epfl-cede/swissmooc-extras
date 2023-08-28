# -*- coding: utf-8 -*-
from apps.split_logs.models import Course
from apps.split_logs.models import Organisation
from rest_framework.serializers import HyperlinkedModelSerializer


class OrganisationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ("id", "name", )


class CourseSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "structure", )
