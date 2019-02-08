# coding: utf-8

import unittest

from tapioca_zendesk import Zendesk


class TestTapiocaZendesk(unittest.TestCase):

    def setUp(self):
        self.wrapper = Zendesk()


if __name__ == '__main__':
    unittest.main()
