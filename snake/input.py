from .kbhit import KBHit

__all__ = ['DefaultKeyReader', 'ArrowKeyReader']


class _KeyReader:
    def capture(self):
        raise NotImplemented

    def last_key(self):
        raise NotImplemented


class DefaultKeyReader(_KeyReader):
    def __init__(self):
        self._kb = KBHit()
        self._last_key = None
        self._tmp = None

    def capture(self):
        self._tmp = None
        if self._kb.kbhit():
            self._last_key = self._kb.getch()

    def last_key(self):
        if self._tmp:
            return self._tmp
        self._tmp = self._last_key
        self._last_key = None
        return self._tmp


class ArrowKeyReader(_KeyReader):
    def __init__(self):
        self._kb = KBHit()
        self._last_key = None
        self._tmp = None

    def capture(self):
        self._tmp = None
        if self._kb.kbhit():
            self._last_key = self._kb.getarrow()

    def last_key(self):
        if self._tmp:
            return self._tmp
        self._tmp = self._last_key
        self._last_key = None
        return self._tmp


if __name__ == '__main__':
    import time
    k = ArrowKeyReader()

    while True:
        now = time.time()

        while time.time() - now < 1:
            k.capture()

        print(k.last_key())
