'''A themeable status bar written in Python, using xcffib.

'''
from . import chunks
from .Bar import Bar
from .FSReader import FSReader
from .Store import Store
from .Window import Window
from .XSetup import XSetup


__all__ = ['chunks', 'Bar', 'FSReader', 'Store', 'Window', 'XSetup']
