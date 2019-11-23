# coding: utf-8

import unittest
import os

from tapioca_zendesk import Zendesk
from tapioca.tapioca import TapiocaClient

class TestTapiocaZendesk(unittest.TestCase):

    def setUp(self):
        self.wrapper = Zendesk()

    def test_zendesk_wrapper(self):
        self.assertIsInstance(self.wrapper, TapiocaClient)

if __name__ == '__main__':
    unittest.main()
