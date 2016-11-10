# -*- coding: utf-8 -*-

from unittest import TestCase

from tm import TuringMachineParser, TuringMachine


TEST_STR = """
% Start with a comment line
  % Another comment line
HALT HALT
BLANK #
INITIAL 1
FINAL 2
1, 0 -> 2, 1, >
1, 1 -> 2, 0, >
2, 0 -> 1, 0, _
 2,1->3,1,>
3, 0 -> HALT, 0, _
3, 1 -> HALT, 1, _
3, # -> HALT, #, _
"""

TEST_UTF8 = """
% Start with a comment line
  % Another comment line
HALT HALT
BLANK 🕴
INITIAL 1
FINAL 2
1, 0 -> 2, 1, >
1, 1 -> 2, 0, >
2, 0 -> 1, 0, _
 2,1->3,1,>
3, 0 -> HALT, 0, _
3, 1 -> HALT, 1, _
3, 🕴 -> HALT, 🕴, _
"""


class TestTuringMachineParser(TestCase):

    def test_parse_string(self):
        parser = TuringMachineParser()
        parser.parse_string(TEST_STR)
        tm = parser.create()

        self.assertTrue(tm.is_word_accepted('0000'))
        self.assertFalse(tm.is_word_accepted('1011'))

    def test_parse_utf8(self):
        parser = TuringMachineParser()
        parser.parse_string(TEST_UTF8)
        tm = parser.create()

        self.assertTrue(tm.is_word_accepted('0000'))
        self.assertFalse(tm.is_word_accepted('1011'))

    def test_create(self):
        parser = TuringMachineParser()
        parser.parse_string(TEST_STR)
        self.assertIsInstance(parser.create(), TuringMachine)
