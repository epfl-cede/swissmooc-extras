# -*- coding: utf-8 -*-
import logging

from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

logger = logging.getLogger(__name__)


def index(request):
    return redirect(reverse("admin:index"))


@login_required
def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.INFO, "You successfuly logged out.")
    return redirect(reverse("home"))


def _error_view(request, context):
    html_template = loader.get_template("home/error.html")
    return HttpResponse(html_template.render(context, request))


def error_500(request):
    context = {
        "error": {
            "title": "Error 500",
            "message": " A server error occurred.  Please contact the administrator.",
        }
    }
    return _error_view(request, context)


def error_400(request, exception):
    context = {
        "error": {
            "title": "Error 400",
            "message": " Bad request",
        }
    }
    return _error_view(request, context)


def error_403(request, exception):
    context = {
        "error": {
            "title": "Error 403",
            "message": " Access denied",
        }
    }
    return _error_view(request, context)


def error_404(request, exception):
    context = {
        "error": {
            "title": "Error 404",
            "message": "Page Not Found",
        }
    }
    return _error_view(request, context)
