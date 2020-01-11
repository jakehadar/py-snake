# -*- coding: utf-8 -*-

import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select

__all__ = ['DefaultKeyReader', 'ArrowKeyReader']


class _KeyReader:
    def capture(self):
        raise NotImplemented

    def last_key(self):
        raise NotImplemented


class DefaultKeyReader(_KeyReader):
    def __init__(self):
        self._kb = _KBHit()
        self._last_key = None
        self._tmp = None

    def capture(self):
        self._tmp = None
        if kb_hit():
            self._last_key = get_ch()

    def last_key(self):
        if self._tmp:
            return self._tmp
        self._tmp = self._last_key
        self._last_key = None
        return self._tmp


class ArrowKeyReader(_KeyReader):
    def __init__(self):
        self._kb = _KBHit()
        self._last_key = None
        self._tmp = None

    def capture(self):
        self._tmp = None
        if kb_hit():
            key = get_arrow()
            if key != -1:
                self._last_key = ['up', 'right', 'down', 'left'][key]

    def last_key(self):
        if self._tmp:
            return self._tmp
        self._tmp = self._last_key
        self._last_key = None
        return self._tmp


def kb_hit():
    """ Returns True if keyboard character was hit, False otherwise.
    """
    if os.name == 'nt':
        return msvcrt.kb_hit()

    else:
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []


def get_ch():
    """ Returns a keyboard character after kb_hit() has been called.
        Should not be called in the same program as get_arrow().
    """

    if os.name == 'nt':
        return msvcrt.get_ch()

    else:
        c = sys.stdin.read(1)
        if ord(c) == 27:
            c2 = sys.stdin.read(1)
            if ord(c2) == 91:
                c3 = sys.stdin.read(1)
                if ord(c3) == 65:
                    return 'up'
                if ord(c3) == 66:
                    return 'down'
                if ord(c3) == 67:
                    return 'right'
                if ord(c3) == 68:
                    return 'left'
                return ord(c3)
            return 'esc'
        elif ord(c) == 10:
            return 'enter'
        return c


def get_arrow():
    """ Returns an arrow-key code after kb_hit() has been called. Codes are
    0 : up
    1 : right
    2 : down
    3 : left
    Should not be called in the same program as get_ch().
    """

    if os.name == 'nt':
        msvcrt.get_ch()  # skip 0xE0
        c = msvcrt.get_ch()
        res = [72, 77, 80, 75]

    else:
        c = sys.stdin.read(3)[2]
        res = [65, 67, 66, 68]

    code = ord(c)
    if code not in res:
        return -1

    return res.index(code)


class _KBHit:
    """
    A Python class implementing KB-HIT, the standard keyboard-interrupt poll-er.
    Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
    with IDLE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    """
    def __init__(self):
        if os.name != 'nt':

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """ Resets to normal terminal.  On Windows this is a no-op.
        """

        if os.name != 'nt':
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


if __name__ == '__main__':
    import time
    k = ArrowKeyReader()

    while True:
        now = time.time()

        while time.time() - now < 1:
            k.capture()

        print(k.last_key())
