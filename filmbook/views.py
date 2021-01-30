from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = "about.html"
    extra_context = {"title": "about"}
