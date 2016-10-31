# -*- coding: utf-8 -*-

import logging
import re
import sys

from tm.tm import TuringMachine
from tm.tmbuilder import TuringMachineBuilder


class TuringMachineParser:
    """
    Proportionate methods to parse a Turing Machine.
    
    The allowed expressions are:
        
        - empty line
        - comment line: '% any text that comes after it's ignored'
        - initial state: 'INITIAL <state>'        
        - blank symbol: 'BLANK <symbol>'
        - final state: 'FINAL <state>'        
        - halt state: 'HALT <state>'
        - transition: '<state>, <symbol> -> <new_state>, <new_symbol>, <movement>
        
    It is not possible to add comments at the end of any line, comments must
    be on a standalone line
    """

    MOVE_RIGHT = '>'
    MOVE_LEFT = '<'
    NON_MOVEMENT = '_'

    #
    #
    def __init__(self):
        self._builder = TuringMachineBuilder()

        # Regular expressions
        self._comment_line_re = re.compile('[ ]*%\s*')
        self._blank_symbol_re = re.compile('[\s]*BLANK[\s]+(?P<symbol>.)\s*$')
        self._halt_state_re = re.compile('[ ]*HALT[ ]+(?P<state>\w+)\s*$')
        self._final_state_re = re.compile('[ ]*FINAL[ ]+(?P<state>\w+)\s*$')
        self._init_state_re = re.compile('[ ]*INITIAL[ ]+(?P<state>\w)\s*$')
        self._transition_re = re.compile('\s*(?P<state>\w+)\s*,\s*'
                                         '(?P<symbol>.)\s*->\s*'
                                         '(?P<nstate>\w+)\s*,\s*'
                                         '(?P<nsymbol>.)\s*,\s*'
                                         '(?P<movement>[%s%s%s])\s*$' %
                                         (TuringMachineParser.MOVE_LEFT,
                                          TuringMachineParser.MOVE_RIGHT,
                                          TuringMachineParser.NON_MOVEMENT)
                                         )

    def clean(self):
        """Cleans all the previous parsed data
        """
        self._builder.clean()

    def parse_string(self, string_data):
        """Parses the given string an adds the information to the Turing
        Machine builder
        
        Raise an exception if the given data is not a string
        """
        if type(string_data) != str:
            raise Exception('Expected an string')

        self._parse(string_data.splitlines())

    def parse_line(self, data):
        """Parse the given line of data
        """
        # The most expected expressions are in order:
        # - Transition
        # - Comments
        # - Final States
        # - Initial State, Halt State, Blank Symbol

        if not self._parse_transition(data):
            if not self._parse_comment(data):
                if not self._parse_final_state(data):
                    if not self._parse_initial_state(data):
                        if not self._parse_blank_symbol(data):
                            if not self._parse_halt_state(data):
                                raise Exception('Unrecognized pattern: %s'
                                                % data)

    def create(self):
        """
        Attempts to create a Turing Machine with the parsed data until the
        call to this function
        
        Can raise any of the TuringMachineBuilder an TuringMachine exceptions
        """
        return self._builder.create()

    def _parse_comment(self, data):
        """
        Returns True if the given data is a comment expression, otherwise
        returns False
        """
        mc = self._comment_line_re.match(data)
        if mc:
            return True
        return False

    def _parse_blank_symbol(self, data):
        """
        Returns True if the given data is a blank symbol expression, otherwise
        returns False
        """
        mbs = self._blank_symbol_re.match(data)
        if mbs:
            if self._builder.has_blank_symbol():
                raise Exception('Blank symbol can only be defined once')

            self._builder.set_blank_symbol(mbs.group('symbol'))
            return True

        return False

    def _parse_halt_state(self, data):
        """
        Returns True if the given data is a halt state expression, otherwise
        returns False
        
        Throws
            Exception if Halt is already defined or if the builder fails when
            setting the halt state
        """
        mhs = self._halt_state_re.match(data)
        if mhs:
            if self._builder.has_halt_state():
                raise Exception('Halt state can only be defined once')

            self._builder.set_halt_state(mhs.group('state'))
            return True

        return False

    def _parse_final_state(self, data):
        """
        Returns True if the given data is a final state expression, otherwise
        returns False
        """
        mfs = self._final_state_re.match(data)
        if mfs:
            self._builder.add_final_state(mfs.group('state'))
            return True

        return False

    def _parse_initial_state(self, data):
        """
        Returns True if the given data is an initial state expression, otherwise
        returns False
        """
        mis = self._init_state_re.match(data)
        if mis:
            if self._builder.has_initial_state():
                raise Exception('Initial state can only be defined once')

            self._builder.set_initial_state(mis.group('state'))
            return True

        return False

    def _parse_transition(self, data):
        """
        Returns True if the given data is a transition state expression,
        otherwise returns False
        """
        mt = self._transition_re.match(data)
        if mt:
            # Filter movement
            move_sym = mt.group('movement')
            move = TuringMachine.NON_MOVEMENT
            if move_sym == TuringMachineParser.MOVE_LEFT:
                move = TuringMachine.MOVE_LEFT
            elif move_sym == TuringMachineParser.MOVE_RIGHT:
                move = TuringMachine.MOVE_RIGHT

            self._builder.add_transition(mt.group('state'),
                                         mt.group('symbol'),
                                         mt.group('nstate'),
                                         mt.group('nsymbol'),
                                         move)
            return True

        return False

    def _parse(self, parse_data):
        """
        Parses the specified data
        
            - parse_data: must be an iterable that returns a new line of data
              on each iteration
        """

        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

        for line, data in enumerate(parse_data):
            # The execution flow it's ugly
            # But personally I hate the idea of have a lot of indentation levels

            if not data:
                continue
            try:
                self.parse_line(data)
            except Exception as e:
                raise Exception('Line %d, %s' % (line + 1, str(e)))


#
# Test                    
if __name__ == '__main__':
    parser = TuringMachineParser()
    test_str = '% Start with a comment line\n' \
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
    parser.parse_string(test_str)

    tm = parser.create()

    print(tm)
