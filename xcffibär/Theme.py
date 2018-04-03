from collections import ChainMap, defaultdict


class ChunkStyle(object):
    def __init__(self, config):
        self.config = config

    def __getattr__(self, name):
        return self.config[name]


class Theme(object):
    def __init__(self, config):
        self.config = config

        self.defaultChunkStyle = defaultdict(lambda: None, config.get('defaultChunkStyle', {}))

        self.chunkStyles = defaultdict(lambda: {}, config.get('chunkStyles', {}))

    def __getattr__(self, name):
        return self.config.get(name, None)

    def getChunkStyle(self, *chunkStyleNames):
        maps = [self.chunkStyles[styleName] for styleName in chunkStyleNames] + [self.defaultChunkStyle]
        return ChunkStyle(ChainMap(*maps))
