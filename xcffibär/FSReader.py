'''Filesystem reader utility class

'''
from .timers import addInterval


class FSReader(object):
    def __init__(self, filename, target, store, transform=None):
        self.filename = filename
        self.target = target
        self.store = store
        self.transform = transform

    def update(self):
        with open(self.filename, 'r') as file:
            value = file.read()
            if callable(self.transform):
                value = self.transform(value)
            self.store[self.target] = value

    def updateEvery(self, delay):
        addInterval(delay, self.update)
