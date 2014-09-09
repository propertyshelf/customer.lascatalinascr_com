# -*- coding: utf-8 -*-
""" Listing Filter Portlet"""

from Acquisition import aq_inner
from plone.z3cform import z2
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.interfaces import IFormLayer
from zope.interface import alsoProvides

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface
try:
    from plone.z3cform.interfaces import IWrappedForm
    HAS_WRAPPED_FORM = True
except ImportError:
    HAS_WRAPPED_FORM = False

try:
    # try to extend plone.mls.listing QuickSearch Renderer
    from plone.mls.listing.portlets.quick_search import Renderer as PortletRenderer, QuickSearchForm as PortletForm
    PLONE_MLS_LISTING = True
except ImportError:
    # fall back to base Renderer
    from plone.app.portlets.portlets.base import Renderer as PortletRenderer
    from plone.directives.form import Form as PortletForm
    PLONE_MLS_LISTING = False

#: Definition of available fields in the given ``rows``.
FIELD_ORDER = {
    'row_listing_type': [
        'listing_type',
        'object_type',
    ],
    'row_beds_baths': [
        'beds',
    ],
    
    'row_object_type': [
        'view_type',
    ],
    'row_price': [
        'price_min',
        'price_max',
    ],  
    'row_pool':[
        'pool'
    ],
    'row_filter': [
        'air_condition',
        'pool',
        'jacuzzi',
        'location_type',
        'geographic_type',
    ],
}

class FilterSearch(PortletRenderer):
    """Class containing customizations for the ListingQuickSearch"""
    render = ViewPageTemplateFile('templates/filterportlet.pt')

    def update(self):
        z2.switch_on(self, request_layer=IFormLayer)
        self.form = FilterSearchForm(aq_inner(self.context), self.request, self.data)

        if HAS_WRAPPED_FORM:
            alsoProvides(self.form, IWrappedForm)
            self.form.update()


class FilterSearchForm(PortletForm):
    """Filter Search Form."""

    def _widgets(self, row):
        """Return a list of widgets that should be shown for a given row."""

        widget_data = dict(self.widgets.items())
        available_fields = FIELD_ORDER.get(row, [])
        return [widget_data.get(field, None) for field in available_fields]
