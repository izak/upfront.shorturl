from zope.interface import implements

from persistent import Persistent
from BTrees.OOBTree import OOBTree, OOSet

from upfront.shorturl.interfaces import IShortURLStorage


class ShortURLStorage(Persistent):
    """Stores short codes and urls to redirect to. """
    implements(IShortURLStorage)

    def __init__(self):
        self._map = OOBTree()

    def add(self, short, target):
        self._map[short] = target

    def remove(self, short):
        if self._map.has_key(short):
            del self._map[short]

    def get(self, short, default=None):
        return self._map.get(short, default)

    def __getitem__(self, key):
        return self._map.items()[key]

    def __len__(self):
        return len(self._map)
