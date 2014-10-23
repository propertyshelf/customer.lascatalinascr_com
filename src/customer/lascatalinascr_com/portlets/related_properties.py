# -*- coding: utf-8 -*-
""" Related Properties Portlet"""

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope import formlib, schema
from zope.schema.fieldproperty import FieldProperty
from zope.component import queryMultiAdapter

#local imports
from plone.mls.listing.i18n import _
from plone.mls.listing.api import search
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

    _isRental    = False
    _isSale      = False
    _listingType = None

    
    @property
    def available(self):
        """Check the portlet availability."""
        """Show on ListingDetails"""
        show = False
        #available for ListingDetails
        if getattr(self.request, 'listing_id', None) is not None:
            show = True

        return show

    @property
    def _listingData(self):
        return getattr(self.context, 'data', None)

    @property
    def _listingInfo(self):
        """get Listing Info"""
        return self._listingData.get('info', None)

    @property
    def title(self):
        """Return the title"""
        if self.data.heading is not None:
            return self.data.heading
        return self.data.title

    @property
    def Limit(self):
        try:
            return int(self.data.limit)
        except Exception:
            pp(Exception)
            return 4

    @property
    def ListingType(self):
        """return ListingType of active listing""" 

        if self._listingType is not None:
            return self._listingType

        elif self._listingInfo is not None:
            #set ListingType
            try:
                listingID = self._listingInfo['id']['value']
                self._listingType = listingID[:2].lower()
            except Exception, e:
                pp(e)

            if self._listingType == 'rl' or self._listingType == 'cl':
                self._isRental = True

            if self._listingType == 'rs' or self._listingType == 'cs' or self._listingType == 'll':
                self._isSale = True

            return self._listingType
        else:
            return None

    @property
    def StartPrice(self):
        """calculate startprice for related listings"""
        price = self._listingInfo['price_raw']['value']
        #set startprice on 90% of the current
        return int(price)+1

    def RelatedListings(self):
        """get Related Listings"""
        ps = queryMultiAdapter((self.context, self.request), name='plone_portal_state')
        lang= ps.language()

        search_params = {
            'limit': self.Limit,
            'lang': lang,
            'agency_listings': True,
            'price_min':self.StartPrice,
            'listing_type':self.ListingType
        }

        results, batch = search(search_params, context=self.context)
        
        items = batch.get('items', 0)
        #check result set
        if items >=self.Limit:
            return results
        elif items < 2:
            # set a min price of $1000 to avoid the listings with empty prices
            price_min = 1000
        else:
            #if we don't have enough results, search again with smaller price
            price_min = self.StartPrice * 0.9

        # reset search params with new start price
        search_params['price_min'] = price_min;
            
        results, batch = search(search_params, context=self.context)
        return results     

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

