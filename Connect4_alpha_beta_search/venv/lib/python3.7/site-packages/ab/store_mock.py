class MockRedis(object):

    def __init__(self):
        self.data = {}

    def set(self, key, val):
        self.data[key] = val
        return val

    def get(self, key):
        return self.data.get(key)

    def incr(self, key):
        val = int(self.get(key) or '0')
        return self.set(key, val + 1)

    def mget(self, keys):
        return [self.get(key) for key in keys]
