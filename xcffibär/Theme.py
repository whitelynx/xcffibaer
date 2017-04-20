class ChunkStyle(object):
    def __init__(self, config, parentStyle=None):
        self.config = config
        self.parentStyle = parentStyle

    def __getattr__(self, name):
        if self.parentStyle:
            return self.config.get(name, getattr(self.parentStyle, name))
        else:
            return self.config.get(name, None)


class Theme(object):
    def __init__(self, config):
        self.config = config

        self.defaultChunkStyle = ChunkStyle(config.get('defaultChunkStyle', {}))

        self.chunkStyles = dict(
            (chunkClass, ChunkStyle(chunkConfig, self.defaultChunkStyle))
            for chunkClass, chunkConfig in config.get('chunkStyles', {}).items()
        )

    def __getattr__(self, name):
        return self.config.get(name, None)

    def chunkStyle(self, chunkClass):
        return self.chunkStyles.get(chunkClass, self.defaultChunkStyle)
