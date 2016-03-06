#!/usr/bin/env python3

import unittest

from pmlr import pmlr

DEBUG = True

print = pmlr.util.writer

debug = (lambda *args, **kwargs: print(*args, **kwargs if DEBUG else ""))

class TestStack(unittest.TestCase):

    pass