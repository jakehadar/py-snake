Snake
-----
An interactive CLI Snake game, tested on Python 2.7 and 3.6 Posix environments.

![Applications list view](https://github.com/jakehadar/py-snake/blob/master/screenshots/screenshot@half.png)


Gameplay
--------
* Use the arrow keys to guide the snake around the game board.
* Score points by collecting food.
* Avoid colliding with walls, or your own body.


Installation
------------
Install from PyPi using
[pip](http://www.pip-installer.org/en/latest/), a package manager for
Python.

``` {.sourceCode .bash}
 $ pip install py-snake
```

Or clone the repo and install using setuptools.

``` {.sourceCode .bash}
 $ cd path/to/repo
 $ python setup.py develop
```

Both methods will create an executable `snake` for your active Python environment. Whenever this environment is active, `snake` will be scoped in your PATH and playable from any working directory.


Usage
-----
After installation, start a new game by running `snake` from any directory on command line. 

``` {.sourceCode .bash}
$ snake
```

Optionally pass the `--help` flag to see options available for game configuration.

``` {.sourceCode .bash}
$ snake --help
usage: snake [-h] [--width WIDTH] [--height HEIGHT] [--speed SPEED]
             [--food FOOD]

Snake game for CLI

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    Frame width
  --height HEIGHT  Frame height
  --speed SPEED    Snake speed (fps)
  --food FOOD      Number of food pieces available
```


Troubleshooting
---------------
If the `snake` command stops working after a successful installation, check that you have the correct Python environment activated. You may need to manually activate the Python environment from a new terminal session, depending on how your environment is configured.


Uninstallation
--------------
Uninstall py-snake using pip.

``` {.sourceCode .bash}
 $ pip uninstall py-snake
```
