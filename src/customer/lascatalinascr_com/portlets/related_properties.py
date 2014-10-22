# -*- coding: utf-8 -*-
""" Related Properties Portlet"""

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope import formlib, schema
from zope.schema.fieldproperty import FieldProperty

#local imports
from plone.mls.listing.i18n import _
from pprint import pprint as pp

MSG_PORTLET_DESCRIPTION = _(u'This portlet shows Related Listings on ListingDetails.')

class IRelatedPropertiesPortlet(IPortletDataProvider):
    """A portlet displaying related properties on ListingDetail"""
    heading = schema.TextLine(
        description=_(
            u'Custom title for the portlet (search mode). If no title is '
            u'provided, the default title is used.'
        ),
        required=False,
        title=_(u'Portlet Title (Search)'),
    )

    limit = schema.TextLine(
        description=_(
            u'How many Properties to show?'
        ),
        required=False,
        title=_(u'Limit'),
        default=u'4'
    )

    agency_listings = schema.Bool(
        description=_(
            u'If activated, only listings of the configured agency are shown.',
        ),
        required=False,
        title=_(u'Agency Listings'),
    )

@implementer(IRelatedPropertiesPortlet)
class Assignment(base.Assignment):
    """Related Listing Portlet Assignment."""

    heading = FieldProperty(IRelatedPropertiesPortlet['heading'])
    try:
        limit = int(FieldProperty(IRelatedPropertiesPortlet['limit']))
    except Exception,e:
        limit = None
    try:
        agency_listings = bool(FieldProperty(IRelatedPropertiesPortlet['agency_listings']))
    except Exception,e:
        agency_listings = True
    
    title = _(u'Related Listings')

    def __init__(self, heading=None, limit=None, agency_listings=None):
        self.heading = heading
        self.limit = limit
        self.agency_listings = agency_listings


class Renderer(base.Renderer):
    """Related Listing Portlet Renderer."""
    render = ViewPageTemplateFile('templates/relatedproperties.pt')

    @property
    def available(self):
        """Check the portlet availability."""
        """Show on ListingDetails"""
        show = False
        #available for ListingDetails
        if getattr(self.request, 'listing_id', None) is not None:
            pp('ListingDetails found')
            pp(self.request)
            #import pdb
            #pdb.set_trace()
            show = True

        return show

    @property
    def title(self):
        """Return the title"""
        if self.data.heading is not None:
            return self.data.heading
        return self.data.title

class AddForm(base.AddForm):
    """Add form for the Listing Related Listing Portlet."""
    form_fields = formlib.form.Fields(IRelatedPropertiesPortlet)
    
    label = _(u'Add Related Listing Portlet')
    description = MSG_PORTLET_DESCRIPTION

    def create(self, data):
        assignment = Assignment()
        formlib.form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """Edit form for the Listing FilterSearch portlet."""
    form_fields = formlib.form.Fields(IRelatedPropertiesPortlet)
    
    label = _(u'Edit FilterSearch portlet')
    description = MSG_PORTLET_DESCRIPTION

