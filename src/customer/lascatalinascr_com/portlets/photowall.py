# -*- coding: utf-8 -*-
""" Photo Wall Portlet """
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope import formlib, schema
from zope.schema.fieldproperty import FieldProperty

# local imports
from plone.mls.listing.i18n import _

MSG_PORTLET_DESCRIPTION = _(u'This portlet let includes a Listing PhotoWall.')


class IPhotoWallPortlet(IPortletDataProvider):
    """ A PhotoWall portlet """
    heading = schema.TextLine(
        description=_(u'Portlet Title'),
        required=False,
        title=_(u'Portlet Title'),
    )


@implementer(IPhotoWallPortlet)
class Assignment(base.Assignment):
    """PhotoWall Portlet Assignment."""

    heading = FieldProperty(IPhotoWallPortlet['heading'])
    title = _(u'PhotoWall Portlet')

    def __init__(self, heading=None):
        self.heading = heading


class Renderer(base.Renderer):
    """PhotoWall Portlet Renderer."""
    render = ViewPageTemplateFile('templates/photowall.pt')

    @property
    def available(self):
        """Check the portlet availability."""
        """Show on ListingDetails"""
        show = False
        # available for ListingDetails
        if getattr(self.request, 'listing_id', None) is not None:
            show = True
        return show

    @property
    def title(self):
        """Return the title"""
        if self.data.heading is not None:
            return self.data.heading
        else:
            return False

    @property
    def images(self):
        """return the current ListingImages"""
        data = getattr(self.context, 'data', None)
        if data is not None:
            images = data.get('images', None)
            return images
        else:
            return None


class AddForm(base.AddForm):
    """Add form for the PhotoWall Portlet."""
    form_fields = formlib.form.Fields(IPhotoWallPortlet)

    label = _(u'Add PhotoWall Portlet')
    description = MSG_PORTLET_DESCRIPTION

    def create(self, data):
        assignment = Assignment()
        formlib.form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """Edit form for the PhotoWall portlet."""
    form_fields = formlib.form.Fields(IPhotoWallPortlet)

    label = _(u'Edit PhotoWall portlet')
    description = MSG_PORTLET_DESCRIPTION
