from copy import deepcopy
import deepmerge


class Config(dict):
    def clone(self):
        return deepcopy(self)

    def merge(self, config):
        deepmerge.always_merger.merge(self, config)
