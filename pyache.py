# Copyright 2019 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import shutil
import numpy as np
from hashlib import md5
from glob import glob
from os import makedirs
from os import name as os_name
from os.path import join, getmtime, isfile
from typing import Callable, Union


class Pyache:
    """
    A class for storing and interacting with a folder numpy cache
    Args:
        folder: Location of cache
        loader: Function that receives a filename and returns a numpy array of consistent size
        loader_id: Unique string associated with loader
        max_loaders: Maximum number of loader caches before others are deleted
    """

    @property
    def file_delimiter(self):
        """
        Returns:
            an OS dependent string used as a delimiter in file names to improve readability.
        """
        if os_name == "nt":
            return "_"
        else:
            return "::"  # Keeping backwards compatibility (invalid file name character on windows)

    def __init__(self, folder: str, loader: Callable, loader_id: str, max_loaders=3):
        self.folder = folder
        self.loader = loader
        self.loader_id = loader_id
        self.max_loaders = max_loaders
        self.loader_folder = join(folder, 'loader{}{}'.format(self.file_delimiter, loader_id))
        self.data_folder = join(self.loader_folder, 'data')
        makedirs(self.data_folder, exist_ok=True)

    def load_file(self, filename, on_gen=lambda x: None) -> Union[np.ndarray, None]:
        """
        Loads a single file
        Args:
            filename: File to load
            on_gen: Function to call on a cache miss. Receives filename as only parameter
        Returns:
            np.ndarray: The loaded array or None if there was a ValueError while loading
        """
        cache_file = join(self.data_folder, md5(filename.encode()).hexdigest() + '.npy')
        if isfile(cache_file):
            return np.load(cache_file)
        try:
            data = self.loader(filename)
        except ValueError:
            return None
        np.save(cache_file, data)
        on_gen(filename)
        return data

    def load(self, filenames: list, on_gen=lambda x: None, on_loop=lambda: None) -> np.ndarray:
        """
        Load a chunk of filenames as a single numpy array, possibly from cache
        Args:
            filenames: List of filenames to load
            on_gen: Function receiving a filename that is run on all cache misses
            on_loop: Function called each loop where a new file was loaded
        Returns:
            np.ndarray: All data from filenames as a single numpy array
        """
        my_suffix = 'cacheblock' + self.file_delimiter + md5(''.join(sorted(filenames)).encode()).hexdigest() + '.npy'
        self._remove_old_resource(self.folder, self.max_loaders, 'loader' + self.file_delimiter,
                                  'loader{}{}/'.format(self.file_delimiter, self.loader_id))

        self._remove_old_resource(self.loader_folder, self.max_loaders, 'cacheblock' + self.file_delimiter, my_suffix)
        cache_file = join(self.loader_folder, my_suffix)
        if isfile(cache_file):
            try:
                return np.load(cache_file)
            except OSError:
                pass
        data = []
        for filename in filenames:
            res = self.load_file(filename, on_gen)
            if res is not None:
                data.append(res)
            on_loop()
        np.save(cache_file, data)
        return np.array(data)

    def cleanup(self):
        self._remove_old_resource(self.folder, self.max_loaders, 'loader' + self.file_delimiter)
        self._remove_old_resource(self.loader_folder, self.max_loaders, 'cacheblock' + self.file_delimiter)

    @staticmethod
    def _remove_old_resource(folder, max_count, prefix, my_suffix=None):
        remaining = max_count - 1  # Doesn't include ourself
        other_loaders = [i for i in glob(join(folder, prefix + '*/')) if not my_suffix or not i.endswith(my_suffix)]
        if len(other_loaders) > remaining:
            to_delete = sorted(other_loaders, key=getmtime)[:len(other_loaders) - remaining]
            for i in to_delete:
                shutil.rmtree(i)
