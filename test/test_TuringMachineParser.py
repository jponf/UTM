# -*- coding: utf-8 -*-

from unittest import TestCase

from tm import TuringMachineParser, TuringMachine


TEST_STR = '% Start with a comment line\n' \
           '  % Another comment line\n' \
           'HALT HALT\n' \
           'BLANK #\n' \
           'INITIAL 1\n' \
           'FINAL 2\n' \
           '1, 0 -> 2, 1, >\n' \
           '1, 1 -> 2, 0, > \n' \
           '2, 0 -> 1, 0, _\n' \
           ' 2,1->3,1,>\n ' \
           '3, 0 -> HALT, 0, _\n' \
           '3, 1 -> HALT, 1, _\n' \
           '3, # -> HALT, #, _\n'


class TestTuringMachineParser(TestCase):

    def test_parse_string(self):
        parser = TuringMachineParser()
        parser.parse_string(TEST_STR)
        tm = parser.create()

        self.assertTrue(tm.is_word_accepted('0000'))
        self.assertFalse(tm.is_word_accepted('1011'))

    def test_create(self):
        parser = TuringMachineParser()
        parser.parse_string(TEST_STR)
        self.assertIsInstance(parser.create(), TuringMachine)
