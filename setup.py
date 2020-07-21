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
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyache',
    version='0.2.0',
    license='Apache2.0',
    description='A simple numpy caching library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mycroft AI',
    author_email='support@mycroft.ai',
    maintainer='Matthew Scholefield',
    maintainer_email='matthew331199@gmail.com',
    url='https://github.com/mycroftai/pyache',
    py_modules=['pyache'],
    install_requires=[
        'numpy'
    ]
)
