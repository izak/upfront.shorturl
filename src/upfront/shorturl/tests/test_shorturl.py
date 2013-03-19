import os
from StringIO import StringIO
import unittest2 as unittest
from plone.testing import z2

from base import INTEGRATION_TESTING


class TestShortURL(unittest.TestCase):
    """ Test URL Shortener product. """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def testStorage(self):
        """ Check that storage exists, and that we can store and remove
            mappings.
        """
        from zope.component import queryUtility
        from upfront.shorturl.interfaces import IShortURLStorage

        # Test that utility exists and that it is empty
        storage = queryUtility(IShortURLStorage)
        self.assertTrue(len(storage)==0, "Initial storage should have zero length.")

        # Test that we can add some mappings
        storage.add('badb0b', 'http://nosite/')
        storage.add('f00f00', 'http://somesite/')
        storage.add('b00b0b', 'http://othersite/')

        self.assertTrue(len(storage)==3,
            "After adding n items, the storage should have length n.")

        # Test that we can look up a mapping
        self.assertTrue(storage.get('f00f00')=='http://somesite/',
            "Failed to look up a mapping")

        # Asking for something non-existent should return None
        self.assertTrue(storage.get('blabla') is None,
            "Looking up a non-existent mapping should return None.")

        # Remove a mapping
        storage.remove('badb0b')
        self.assertTrue(len(storage)==2,
            "Removing an item from the storage should reduce its size.")

        # Test that we can iterate over it, if we can't, this will fail
        for i,j in storage:
            pass

    def testAddAndRemove(self):
        """ Test that the browser views are there and work correctly. """
        from zExceptions import Unauthorized
        from zope.component import queryUtility
        from upfront.shorturl.interfaces import IShortURLStorage
        storage = queryUtility(IShortURLStorage)
        request = self.layer['request']
        request["form.submitted"] = "1"
        request["shortcode"] = "aaaaa"
        request["target"] = "http://aaaaa"
        request['ACTUAL_URL'] = request['SERVER_URL']

        # You can't do this unless you have ManagePortal
        self.assertRaises(
            Unauthorized,
            lambda: self.portal.restrictedTraverse('@@add-shorturl'))

        member = self.portal.restrictedTraverse('@@plone_portal_state').member()
        roles = member.getRoles()
        z2.setRoles(self.portal.acl_users, member.getId(),
            roles + ['Manager'])
        addview = self.portal.restrictedTraverse('@@add-shorturl')
        addview()
        self.assertTrue(len(request.get('errors', {}))==0,
            "Adding a short url raised errors")

        # Add it again, it should return an error
        addview()
        self.assertTrue(len(request.get('errors', {}))!=0,
            "Adding a duplicate shortcode should raise an error.")

        self.assertTrue(len(storage)==1, "Adding mapping failed.")

        # Delete it
        request.clear()
        request["remove"] = ["aaaaa"]
        self.portal.restrictedTraverse('@@manage-shorturls').update()
        self.assertTrue(len(storage)==0, "Deleting mapping failed.")

    def testRedirect(self):
        from zope.component import queryUtility
        from upfront.shorturl.interfaces import IShortURLStorage
        storage = queryUtility(IShortURLStorage)
        request = self.layer['request']

        # Add a few redirects
        storage.add('badb0b', 'http://nosite/')
        storage.add('f00f00', 'http://somesite/')
        storage.add('b00b0b', 'http://othersite/')

        # Try a redirect
        request["shortcode"] = "f00f00"
        self.portal.restrictedTraverse('@@shorturl')()
        self.assertTrue(request.response['location']=='http://somesite/',
            "Redirect view did not correctly redirect.")

        # And if the code doesn't exist...
        request["shortcode"] = "f00f01"
        self.portal.restrictedTraverse('@@shorturl')()
        self.assertTrue(request.get('error', None) is not None,
            "Looking up a non-existend short code should return an error message.")

    def testCSVImport(self):
        from zope.component import queryUtility
        from upfront.shorturl.interfaces import IShortURLStorage
        storage = queryUtility(IShortURLStorage)
        
        member = self.portal.restrictedTraverse('@@plone_portal_state').member()
        z2.setRoles(self.portal.acl_users, member.getId(),
            member.getRoles() + ['Manager'])
        addview = self.portal.restrictedTraverse('@@add-shorturl')
        f = StringIO("10,http://wasabishop\n22,http://was12\n")
        error = addview._import(f)
        self.assertTrue(len(storage)==2, "CSV import failed to import 2 items")
        self.assertTrue(error is None, "Upload returned an error")

        g = StringIO("101,http://apeaceprize\n22_11_2,http://theend\n")
        error = addview._import(g)
        self.assertTrue(error is not None, "Upload should return an error")

    def test_suggest(self):
        from zope.component import queryUtility
        from upfront.shorturl.interfaces import IShortURLStorage
        storage = queryUtility(IShortURLStorage)

        d = {}
        for i in range(100000):
            key = storage.suggest()
            assert storage.get(key) is None, "key = %s" % key
            storage.add(key, i)
