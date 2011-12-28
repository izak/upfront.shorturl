import string
from zope.interface import implements

from persistent import Persistent
from BTrees.OOBTree import OOBTree, OOSet

from upfront.shorturl.interfaces import IShortURLStorage

def _increment(code):
    """ Take a text string, and guess the next one, assuming we're using only
        alphanumeric characters. If you can't do it, return None.
    """
    if code.isalnum():
        i = 0
        result = ''
        vocab = string.letters + string.digits
        for c in code:
            i = i*len(vocab) + vocab.index(c)
        i += 1
        while i > 0:
            j = i % len(vocab)
            i = i / len(vocab)
            result = vocab[j] + result
        return result
    return None

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

    def suggest(self):
        try:
            key = self._map.maxKey()
        except ValueError:
            # If the tree is empty
            return 'AAAAA'
        return _increment(key)

    def __getitem__(self, key):
        return self._map.items()[key]

    def __len__(self):
        return len(self._map)
