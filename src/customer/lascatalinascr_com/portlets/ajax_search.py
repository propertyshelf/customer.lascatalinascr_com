# -*- coding: utf-8 -*-
"""View for AjaxSearch"""
from plone.memoize.view import memoize
from Products.Five.browser import BrowserView, pagetemplatefile
from zope.component import queryMultiAdapter
from zope.traversing.browser.absoluteurl import absoluteURL

#plone.mls.listing imports
from plone.mls.core.navigation import ListingBatch
from plone.mls.listing.api import prepare_search_params, search

def encode_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict

class ajaxSearch(BrowserView):
    """Deliver search results for ajax calls"""
    index = pagetemplatefile.ViewPageTemplateFile("templates/ajax_template.pt")

    _listings = None
    _batching = None


    def __init__(self, context, request):
        super(ajaxSearch, self).__init__(context, request)
        self.context = context
        self.request = request
        self.update()
        

    def __call__(self):
        return self.render()

    def update(self):
        self.portal_state = queryMultiAdapter((self.context, self.request),
                                                name='plone_portal_state')
        self.context_state = queryMultiAdapter((self.context, self.request),
                                               name='plone_context_state')

        self.request.form = encode_dict(self.request.form)

        request_params = self._get_params
        self._get_listings(request_params)

    @property
    def limit(self):
        return 15

    def render(self):
        """Prepare view related data.""" 
        return self.index()

    @property
    def _get_params(self):
        """map MLS search with custom UI"""
        params={}
        return prepare_search_params(params)

    def _get_listings(self, params):
        """Query the recent listings from the MLS."""
        search_params = {
            'limit': self.limit,
            'offset': self.request.get('b_start', 0),
            'lang': self.portal_state.language(),
            'agency_listings': False
        }
        search_params.update(params)
        results, batching = search(search_params, context=self.context)
        self._listings = results
        self._batching = batching

    @property
    @memoize
    def listings(self):
        """Return listing results."""
        return self._listings

    @memoize
    def view_url(self):
        """Generate view url."""
        if not self.context_state.is_view_template():
            return self.context_state.current_base_url()
        else:
            return absoluteURL(self.context, self.request) + '/'

    @property
    def batching(self):
        return ListingBatch(self.listings, self.limit,
                            self.request.get('b_start', 0), orphan=1,
                            batch_data=self._batching)
