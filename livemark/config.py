from copy import deepcopy
import deepmerge


class Config(dict):
    def merge(self, config):
        return Config(deepmerge.always_merger.merge(deepcopy(self), config))
