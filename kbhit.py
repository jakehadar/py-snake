#!/usr/bin/env python
'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
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

'''

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


class KBHit:
    _lock = False
    
    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass
        
        else:
    
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
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''
        
        if os.name == 'nt':
            pass
        
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''
        
        s = ''
        
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        
        else:
            c = bytes(sys.stdin.read(1), encoding='utf8')
            if ord(c.decode('utf-8')) == 27:
                c2 = bytes(sys.stdin.read(1), encoding='utf8')
                if ord(c2.decode('utf-8')) == 91:
                    c3 = bytes(sys.stdin.read(1), encoding='utf8')
                    if ord(c3.decode('utf-8')) == 65:
                        return 'up'
                    if ord(c3.decode('utf-8')) == 66:
                        return 'down'
                    if ord(c3.decode('utf-8')) == 67:
                        return 'right'
                    if ord(c3.decode('utf-8')) == 68:
                        return 'left'
                    return ord(c3.decode('utf-8'))
                return 'esc'
            elif ord(c.decode('utf-8')) == 10:
                return 'enter'
            return c.decode('utf-8')
                        

    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''
        
        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]
            
        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]
        
        return vals.index(ord(c.decode('utf-8')))
        

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()
        
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


class KBHitSequencer:
    def __init__(self, sequence_gen=None):
        self.sequence_gen = sequence_gen if sequence_gen else iter([])
        self.first_iteration = True
        self._lock = False
        self.cache = []

    def next_value(self):
        try:
            return next(self.sequence_gen)
        except StopIteration:
            return None

    def kbhit(self):
        if self._lock:
            return False

        if len(self.cache) == 0:
            next_val = self.next_value()
            self.cache.append(next_val)

        if self.first_iteration:
            self.first_iteration = False
            return True

        return len(self.cache) > 0 or self.first_iteration

    def getch(self):
        if len(self.cache) > 0:
            value = self.cache.pop()
            self._lock = True
            return value
    
    
# Test    
if __name__ == "__main__":
    
    kb = KBHit()

    print('Hit any key, or ESC to exit')

    while True:

        if kb.kbhit():
            c = kb.getch()
            if c == 'esc':
                break
            print(c)
             
    kb.set_normal_term()
        

