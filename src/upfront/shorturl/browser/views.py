from zope.component import queryUtility
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from upfront.shorturl.interfaces import IShortURLStorage

class EditView(BrowserView):
    pass

class RedirectView(BrowserView):
    template = ViewPageTemplateFile("redirect.pt")

    def __call__(self):
        return self.template()
