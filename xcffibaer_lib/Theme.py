'''Theme class

'''
from collections import ChainMap, defaultdict


class ChunkStyle:
    def __init__(self, config):
        self._config = config
        for key, value in config.items():
            setattr(self, key, value)

    def __getattr__(self, name):
        return None


class Theme:
    def __init__(self, config):
        self.config = config

        self.defaultChunkStyle = config.get('defaultChunkStyle', {})

        self.chunkStyles = defaultdict(lambda: {}, config.get('chunkStyles', {}))

    def __getattr__(self, name):
        return self.config.get(name, None)

    def getChunkStyle(self, *chunkStyleNames):
        maps = [self.chunkStyles[styleName] for styleName in chunkStyleNames] + [self.defaultChunkStyle]
        return ChunkStyle(ChainMap(*maps))
