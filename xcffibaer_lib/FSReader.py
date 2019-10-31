'''Filesystem reader utility class

'''
from .timers import addInterval
from .utils import printError


class FSReader:
    def __init__(self, filename, target, store, transform=None):
        self.filename = filename
        self.target = target
        self.store = store
        self.transform = transform
        self.lastError = None

    def update(self):
        try:
            with open(self.filename, 'r') as file:
                value = file.read()
                if callable(self.transform):
                    value = self.transform(value)
                self.store[self.target] = value
            self.lastError = None
        except OSError as error:
            if self.lastError != error.strerror:
                printError(f'{error.__class__.__name__} reading {self.filename}:', error)
                self.lastError = error.strerror

    def updateEvery(self, delay):
        addInterval(delay, self.update)
