from zope.interface import Interface, Attribute


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

    def __iter__():
        """ Iterator for working through all mappings. """
