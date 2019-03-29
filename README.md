# Pyache

*Python numpy caching library*

This library caches numpy data that is generated from files and saves them in chunks to the disk.
This is useful any time a computationally expensive task is done to files to transform them into a form needed in memory.

# Usage

Create a `Pycache` object and call `load` with your filenames.

```python
import numpy as np
from time import sleep
from pyache import Pyache


def load_file(filename) -> np.ndarray:
    print('Processing {}...'.format(filename))
    sleep(0.5)
    return np.ones([100])


pyache = Pyache('.cache', load_file, 'ones-processor')
data = pyache.load(
    ['thing-1.png', 'thing-2.png', 'thing-3.png'],
    on_gen=lambda x: print('Just reprocessed', x),
    on_loop=lambda: print('Loaded one more...')
)  # Takes 1.5 seconds

# ... Run a second time (or program re-run):
data = pyache.load(
    ['thing-1.png', 'thing-2.png', 'thing-3.png']
)  # Takes 0.0 seconds

data = pyache.load(
    ['thing-1.png', 'thing-2.png', 'thing-3.png', 'thing-4.png']
)  # Takes 0.5 seconds
```

# Installation

```bash
pip install pyache
```
