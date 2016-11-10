# -*- coding: utf-8 -*-


class HaltStateException(Exception):
    """Exception raised when trying to continue execution from halt state"""


class TapeNotSetException(Exception):
    """Exception raised when the tape is not set"""


class InvalidSymbolException(Exception):
    """Exception raised when a symbol is not valid"""


class UnknownTransitionException(Exception):
    """Exception raised when there is no specified transition
    with a given (state, symbol) tuple
    """
