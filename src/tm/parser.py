# -*- coding: utf-8 -*-

import re

from tm.tm import TuringMachine
from tm.builder import TuringMachineBuilder


# Parser regular expressions
##############################################################################

_MOVE_RIGHT = '>'
_MOVE_LEFT = '<'
_NON_MOVEMENT = '_'

_COMMENT_RE = re.compile(r'[ ]*%\s*')
_HALT_RE = re.compile(r'[ ]*HALT[ ]+(?P<state>\w+)\s*$')
_INIT_RE = re.compile(r'[ ]*INITIAL[ ]+(?P<state>\w)\s*$')
_FINAL_RE = re.compile(r'[ ]*FINAL[ ]+(?P<state>\w+)\s*$')

_BLANK_SYM_RE = re.compile(r'[\s]*BLANK[\s]+(?P<symbol>.)\s*$')

_TRANSITION_RE = re.compile(
    r'\s*(?P<state>\w+)\s*,\s*(?P<symbol>.)\s*->\s*(?P<new_state>\w+)\s*'
    r',\s*(?P<new_symbol>.)\s*,\s*(?P<movement>[%s%s%s])\s*$' %
    (_MOVE_LEFT, _MOVE_RIGHT, _NON_MOVEMENT))


# Parser Class
##############################################################################

class TuringMachineParser:
    """Parses a string or file containing the description of a turing machine
    
    The allowed expressions are:
        
        - empty line
        -  comment line: '% any text that comes after it's ignored'
        - initial state: 'INITIAL <state>'        
        -  blank symbol: 'BLANK <symbol>'
        -   final state: 'FINAL <state>'
        -    halt state: 'HALT <state>'
        -    transition: '<state>, <symbol> -> <new_state>, <new_symbol>, <movement>
        
    It is not possible to add comments at the end of any line, comments must
    be on a standalone line
    """

    def __init__(self):
        self._builder = TuringMachineBuilder()

    def clean(self):
        """Cleans all the previous parsed data"""
        self._builder.clean()

    def parse_string(self, text):
        """Parses the given string an adds the information to the Turing
        Machine builder

        :raise Exception: if the given data is not a string
        Raise an exception if the given data is not a string
        """
        if not isinstance(text, str):
            raise Exception('Expected an string')

        self._parse(text.splitlines())

    def parse_line(self, line):
        """Parse the given line"""
        parsers = map(lambda f: f(self._builder, line), _PARSE_FUNCTIONS)
        if not any(parsers):
            raise Exception('Unrecognized pattern: %s' % line)

    def create(self):
        """Attempts to create a Turing Machine with the data parsed before the
        call to this function
        
        Can raise any of the TuringMachineBuilder an TuringMachine exceptions
        """
        return self._builder.create()

    def _parse(self, parse_data):
        reader = ((i, l.strip()) for i, l in enumerate(parse_data, start=1))
        reader = ((i, l) for i, l in reader if l)

        for i, l in reader:
            try:
                self.parse_line(l)
            except Exception as e:
                raise Exception('Line %d, %s' % (i, str(e)))


# Parsing utilities
##############################################################################

def _parse_comment(_, line):
    return True if _COMMENT_RE.match(line) else False


def _parse_blank_symbol(builder, line):
    m = _BLANK_SYM_RE.match(line)
    if m:
        if builder.has_blank_symbol():
            raise Exception('Blank symbol can only be defined once')

        builder.set_blank_symbol(m.group('symbol'))
        return True

    return False


def _parse_halt_state(builder, line):
    m = _HALT_RE.match(line)
    if m:
        if builder.has_halt_state():
            raise Exception('Halt state can only be defined once')

        builder.set_halt_state(m.group('state'))
        return True

    return False


def _parse_final_state(builder, line):
    m = _FINAL_RE.match(line)
    if m:
        builder.add_final_state(m.group('state'))
        return True

    return False


def _parse_initial_state(builder, line):
    m = _INIT_RE.match(line)
    if m:
        if builder.has_initial_state():
            raise Exception('Initial state can only be defined once')

        builder.set_initial_state(m.group('state'))
        return True

    return False


def _parse_transition(builder, line):
    m = _TRANSITION_RE.match(line)
    if m:
        move_sym, move = m.group('movement'), None
        if move_sym == _MOVE_LEFT:
            move = TuringMachine.MOVE_LEFT
        elif move_sym == _MOVE_RIGHT:
            move = TuringMachine.MOVE_RIGHT
        elif move_sym == _NON_MOVEMENT:
            move = TuringMachine.NON_MOVEMENT

        if move is None:
            raise Exception("Unknown movement %s" % move_sym)

        builder.add_transition(
            m.group('state'), m.group('symbol'),
            m.group('new_state'), m.group('new_symbol'), move)
        return True

    return False


_PARSE_FUNCTIONS = (
    _parse_transition, _parse_comment, _parse_final_state,
    _parse_initial_state, _parse_blank_symbol, _parse_halt_state
)
