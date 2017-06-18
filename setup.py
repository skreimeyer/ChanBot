#!/usr/lib/env python

import os
from setuptools import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__),filename)).read()

setup(
    name = "ChanBot",
    version = "0.0.1",
    author = "Samuel Kreimeyer",
    author_email = "samuel.kreimeyer@gmail.com",
    description = ("A collection of companion scripts for the "
                   "Chatterbot module for generating language "
                   "corpora for chatbot training."),
    license = "GPL 3.0",
    keywords = "Chatterbot, imageboard text processor",
    url = "https://github.com/skreimeyer/ChanBot",
    packages=['CorpusGenerator','InfChanConvo'],
    long_description=read('README.md'),
    install_requires=[
        'bs4',
        'fake_useragent',
        'chatterbot'
        ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Consule",
        ],
    )
