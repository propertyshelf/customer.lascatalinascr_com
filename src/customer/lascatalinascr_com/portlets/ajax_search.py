# -*- coding: utf-8 -*-
"""View for AjaxSearch"""

from Products.Five.browser import BrowserView, pagetemplatefile

class ajaxSearch(BrowserView):
    """Deliver search results for ajax calls"""
    index = pagetemplatefile.ViewPageTemplateFile("templates/ajax_template.pt")

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()
