from zope.interface import Interface, Attribute

class IShortURLLayer(Interface):
    """ Marker interface for this product. """

class IShortURLStorage(Interface):
    """A storage for items where the old and the new location are known.

    Will be registered as a local utility.
    """

    def add(short, target):
        """Add a short code and the target to redirect to. """

    def remove(short):
        """Remove a short code, and its target. """

    def get(short, default=None):
        """ Return the target for the given short, or default if not found. """

    def suggest():
        """ Suggests a new short code for an item. """

    def __getitem__(self, key):
        """ Return a tuple corresponding to the key'th key/value pair. """

    def __len__(self):
        """ Return the number of items in storage. """
