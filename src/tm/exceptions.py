# -*- coding: utf-8 -*-


class HaltStateException(Exception):
    """Exception thrown when trying to continue execution from halt state"""


class TapeNotSetException(Exception):
    """Exception thrown when the tape is not set"""


class InvalidSymbolException(Exception):
    """Exception thrown when a symbol is not valid"""


class UnknownTransitionException(Exception):
    """Exception thrown when there is no specified transition
    with a given (state, symbol) tuple
    """
