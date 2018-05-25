'''Store class

'''
from collections import defaultdict
from string import Formatter

from .timers import addImmediate


class StoreFormatter(Formatter):
    def get_field(self, field_name, args, kwargs):
        return (kwargs[field_name], field_name)


storeFormatter = StoreFormatter()


class TemplateString(object):
    def __init__(self, store, template):
        self.store = store
        self.template = template

    def __str__(self):
        return storeFormatter.vformat(self.template, None, self.store)

    def __repr__(self):
        return str(self)


class Ref(object):
    def __init__(self, store, keyExpr):
        self.store = store
        self.keyExpr = keyExpr

    def __call__(self):
        return self.store[self.keyExpr]

    def watch(self, callback):
        self.store.watch(self.keyExpr, callback)


class Store(object):
    '''A data store.

    '''
    def __init__(self, callback):
        self.callback = callback
        self.watchers = defaultdict(list)
        self.awaitingUpdate = False
        self.awaitingWatchers = defaultdict(bool)
        self.data = {}

    def __getitem__(self, keyExpr):
        data = self.data
        for key in keyExpr.split('.'):
            data = data.get(key)
            if data is None:
                return None
        return data

    def __setitem__(self, keyExpr, value):
        keyExpr = keyExpr.split('.')
        data = self.data
        for key in keyExpr[:-1]:
            data = data.setdefault(key, {})

        if keyExpr[-1] in data:
            # Schedule watchers for any keys contained in the old value.
            self.scheduleNestedWatchers(keyExpr, data[keyExpr[-1]])

        # Actually change the value.
        data[keyExpr[-1]] = value

        # Schedule watchers for the key being set, and its ancestors.
        currentKey = []
        for key in keyExpr:
            currentKey.append(key)
            self.scheduleWatchers('.'.join(currentKey))

        # Schedule watchers for any keys contained in the new value.
        self.scheduleNestedWatchers(currentKey, value)

        if not self.awaitingUpdate:
            self.awaitingUpdate = True
            addImmediate(self.update)

    def callWatchers(self, keyExpr):
        self.awaitingWatchers[keyExpr] = False
        for callback in self.watchers[keyExpr]:
            callback()

    def scheduleWatchers(self, keyExpr):
        if not self.awaitingWatchers[keyExpr]:
            self.awaitingWatchers[keyExpr] = True
            addImmediate(lambda: self.callWatchers(keyExpr))

    def scheduleNestedWatchers(self, currentKey, currentValue):
        if isinstance(currentValue, dict):
            for key, value in currentValue.items():
                self.scheduleWatchers('.'.join(currentKey + [key]))
                self.scheduleNestedWatchers(currentKey + [key], value)

    def template(self, templateStr):
        return TemplateString(self, templateStr)

    def watch(self, keyExpr, callback):
        self.watchers[keyExpr].append(callback)

    def ref(self, keyExpr):
        return Ref(self, keyExpr)

    def update(self):
        self.awaitingUpdate = False
        self.callback()
