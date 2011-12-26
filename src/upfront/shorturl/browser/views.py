import re
from zExceptions import NotFound
from zope.component import queryUtility
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.PloneBatch import Batch
from upfront.shorturl.interfaces import IShortURLStorage
from upfront.shorturl import MessageFactory as _

SHORTURLRE=re.compile(r'^[a-zA-Z0-9]+$')

class EditView(BrowserView):
    def update(self):
        """ Called from the template, it deletes any mappings
            specified on the request. """
        remove = self.request.get('remove', ())
        storage = queryUtility(IShortURLStorage)
        for item in remove:
            storage.remove(item)

    def mappings(self):
        storage = queryUtility(IShortURLStorage)
        b_size = int(self.request.get('b_size', 50))
        b_start = int(self.request.get('b_start', 0))
        return Batch(storage, b_size, b_start)

class AddView(BrowserView):
    template = ViewPageTemplateFile("add.pt")

    def __call__(self):
        if self.request.get('form.submitted', None) is not None:
            shortcode = self.request.get('shortcode', '')
            target = self.request.get('target', '')
            errors = {}
            if not shortcode:
                errors.update(
                    {'shortcode': _(u'You must provide a short code.')})
            if not target:
                errors.update({'target': _(u'You must provide a target.')})
            if SHORTURLRE.match(shortcode) is None:
                errors.update({'shortcode':
                    _(u'Short codes may only contain alphanumeric characters.')})
            if not errors:
                storage = queryUtility(IShortURLStorage)
                if storage.get(shortcode):
                    errors.update(
                        {'shortcode': _(u'This short code is already in use.')})
                else:
                    storage.add(shortcode, target)
                    self.request.response.redirect(
                        '%s/@@manage-shorturls' % self.context.absolute_url())
                    return ''
                    
        self.request['errors'] = errors
        return self.template()

class RedirectView(BrowserView):
    implements(IPublishTraverse)
    template = ViewPageTemplateFile("redirect.pt")

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.traversecode = None

    def lookup(self, code):
        if SHORTURLRE.match(code) is None:
            return None
        storage = queryUtility(IShortURLStorage)
        return storage.get(code, None)

    def publishTraverse(self, request, name):
        """ This method is called if someone appends the shortcode to the end
            of the url. To prevent the silliness of multiple parts being
            appended, we raise NotFound if we already have one. """
        if self.traversecode is None:
            self.traversecode = name
        else:
            raise NotFound(name)
        return self

    def __call__(self):
        shortcode = self.request.get('shortcode', None) or self.traversecode
        error = None
        if shortcode:
            target = self.lookup(shortcode)
            if target is not None:
                self.request.response.redirect(target)
                return ''
            else:
                error = _(u'Shortcode does not exist')

        self.request['error'] = error
        self.request['shortcode'] = shortcode
        return self.template()
