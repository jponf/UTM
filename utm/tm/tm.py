#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from abc import ABCMeta, abstractmethod

from utm.tm.exceptions import (
    HaltStateException,
    InvalidSymbolException,
    UnknownTransitionException,
    TapeNotSetException,
)


# TODO: rewrite doc


class TuringMachine:
    """
    Represents a turing machine, to work properly there are some restrictions:
        - symbols on input alphabet and tape alphabet must be one char length

        - transition function must be a dictionary with the following format:
                        (state, symbol) : (state, symbol, movement)

        - tape movements are defined by the following "constants":
            - MOVE_LEFT
            - MOVE_RIGHT
            - NON_MOVEMENT
    """

    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    NON_MOVEMENT = 3
    HEAD_MOVEMENTS = frozenset((MOVE_LEFT, MOVE_RIGHT, NON_MOVEMENT))

    def __init__(
        self,
        states,
        in_alphabet,
        tape_alphabet,
        trans_function,
        init_state,
        final_states,
        halt_state,
        blank_sym,
    ):
        """
        TuringMachine(states, in_alphabet, tape_alphabet, trans_function,
                    istate, fstate, hstate, blank)

        Initialize an instance of TuringMachine with the given data
            - states:
                Iterable with the possible states
            - in_alphabet:
                Iterable with the input alphabet
            - tape_alphabet:
                Iterable with the machine tape alphabet
            - trans_function:
                Dictionary representing the transition function
                    (state, symbol) : (state, symbol, movement)
            - istate:
                Initial state
            - fstates:
                Iterable with the possible final states
            - hstate:
                Halt state. If reached, execution stops immediatly
            - blank:
                Default symbol in all unspecified tape positions
        """
        self._states = frozenset(states)
        self._in_alphabet = frozenset(in_alphabet)
        self._tape_alphabet = frozenset(tape_alphabet)
        self._trans_function = copy.copy(trans_function)
        self._init_state = init_state
        self._final_states = frozenset(final_states)
        self._halt_state = halt_state
        self._blank_sym = blank_sym

        self._check_data()

        # Machine tape, head and current state
        self._tape = None
        self._head = 0
        self._cur_state = init_state
        self._num_executed_steps = 0

        # Set of observers
        # is a list because other structures like set forces to implement
        # the __hash__ operation
        self._observers = []

    def run_step(self):
        """
        Performs one execution step.

            - If it's at Halt state raises HaltStateException
            - If tape is unset raises UnsetTapeException
            - If there are no specified transition for the current state and
              symbol, raises UnknownTransitionException
        """
        if self.is_at_halt_state():
            raise HaltStateException("Current state is halt state")
        if self._tape is None:
            raise TapeNotSetException("Tape must be set before perform an step")

        cur = (self._cur_state, self._tape[self._head])
        for obs in self._observers:
            obs.on_step_start(cur[0], cur[1])

        try:
            state, sym, movement = self._trans_function[cur]

            self._tape[self._head] = sym
            self._cur_state = state

            prev_head_pos = self._head

            if movement == TuringMachine.MOVE_LEFT:
                if self._head == 0:
                    self._tape.insert(0, self._blank_sym)
                else:
                    self._head -= 1

            elif movement == TuringMachine.MOVE_RIGHT:
                self._head += 1
                if self._head == len(self._tape):
                    self._tape.append(self._blank_sym)

            # Notify observers
            for obs in self._observers:
                obs.on_step_end(state, sym, movement)

                if prev_head_pos != self._head:
                    obs.on_head_moved(self._head, prev_head_pos)

            self._num_executed_steps += 1

        except KeyError:
            raise UnknownTransitionException(
                "There are no transition for %s" % str(cur)
            )

    def run(self, max_steps=None):
        """
        run(max_steps=None): int

        Perform steps until 'halt' or 'max steps'

        Return values:
            0 - Ends by halt state
            1 - Ends by max steps limit
            2 - Ends by unknown transition
        """
        try:
            if max_steps:
                try:
                    for _ in range(max_steps):
                        self.run_step()
                    return 1
                except HaltStateException:
                    return 0

            else:
                while not self.is_at_halt_state():
                    self.run_step()
                return 0

        except UnknownTransitionException:
            return 2

    def get_current_state(self):
        """
        Returns the current state (Cpt. Obvious)
        """
        return self._cur_state

    def get_blank_symbol(self):
        """
        Returns the blank symbol
        """
        return self._blank_sym

    def get_halt_state(self):
        """
        Returns the halt state
        """
        return self._halt_state

    def get_initial_state(self):
        """
        Returns the initial state
        """
        return self._init_state

    def get_symbol_at(self, pos):
        """
        Returns the symbol at the specified position

        The internal symbols goes from 0 to getInternalTapeSize() - 1
        for any other position out of this range the blank symbol is returned
        """
        if pos < 0 or pos >= len(self._tape):
            return self._blank_sym

        return self._tape[pos]

    def get_internal_tape_size(self):
        """
        Returns the size of the internal tape representation
        """
        return len(self._tape)

    def get_head_position(self):
        """
        Returns the current head position
        """
        return self._head

    def get_tape_iterator(self):
        """Returns an iterator of the internal tape"""
        if self._tape:
            return iter(self._tape)
        else:
            raise TapeNotSetException("Tape must be set before getting its iterator")

    def get_executed_steps_counter(self):
        """
        Return the amount of steps executed until the creation of the machine
        or the last call to resetExecutedStepsCounter()
        """
        return self._num_executed_steps

    def is_at_halt_state(self):
        """
        Returns true only if current state is the halt state
        """
        return self._cur_state == self._halt_state

    def is_at_final_state(self):
        """
        Returns true only if current state is a final state
        """
        return self._cur_state in self._final_states

    def is_tape_set(self):
        """
        Returns true only if tape is set
        """
        return self._tape is not None

    def is_word_accepted(self, word, max_steps=None):
        """Tests if the given word is accepted by this turing machine.

        :param word: An iterable str/list/tuple/... of symbols.
        :param max_steps: Limit of steps to test if the word is accepted.

        :return: True if accepted, False otherwise.
        """
        old_tape, old_head = self._tape, self._head
        old_state = self._cur_state

        self.set_tape(word)
        self.run(max_steps)
        accepted = self.is_at_final_state()

        self._tape, self._head = old_tape, old_head
        self._cur_state = old_state

        return accepted

    def set_tape(self, tape, head_pos=0):
        """Sets tape content and head position.

        If head position is negative or greater than tape length the tape is
        filled with blanks.

        :raise InvalidSymbolException: if tape contains an invalid symbol.
        """

        for s in tape:
            if s not in self._tape_alphabet:
                raise InvalidSymbolException("Invalid tape symbol " + str(s))

        # If head pos is out of tape make tape grow with blanks
        if head_pos < 0:
            self._tape = [self._blank_sym] * (-head_pos)
            self._tape.extend(tape)
            self._head = 0
        elif head_pos >= len(tape):
            self._tape = list(tape)
            if not self._tape:
                self._tape = [self._blank_sym]  # Empty tape
            self._tape.extend([self._blank_sym] * (head_pos - len(tape)))
            self._head = head_pos
        else:
            self._tape = list(tape)
            self._head = head_pos

        for obs in self._observers:
            obs.on_tape_changed(head_pos)

    def set_at_initial_state(self):
        """Forces the machine state to be the initial state."""
        self._cur_state = self._init_state

    def attach_observer(self, observer):
        """Attaches an observer to this Turing Machine."""
        # Observer must have the following method
        if not isinstance(observer, BaseTuringMachineObserver):
            raise TypeError("Observer must be subclass of BaseTuringMachineObserver")

        if observer not in self._observers:
            self._observers.append(observer)

    def detach_observer(self, observer):
        """Removes the specified observer"""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def reset_executed_steps_counter(self):
        """Set the executed steps counter to 0"""
        self._num_executed_steps = 0

    def _check_data(self):
        """
        Checks if the given information is correct

            1- Input alphabet is subset of tape alphabet
            2- Blank symbol is into the tape alphabet
            3- Initial state is in states
            4- Final states are all in states
            5- Transition states are defined in states
            6- Transition symbols are defined in tape alphabet
            7- Transition is composed by elements with the specified format:
                    (state, symbol) : (nstate, nsymbol, movement)


        If one of the above fails raises an exception
        """
        movements = frozenset(
            [
                TuringMachine.MOVE_LEFT,
                TuringMachine.MOVE_RIGHT,
                TuringMachine.NON_MOVEMENT,
            ]
        )

        if not self._in_alphabet.issubset(self._tape_alphabet):
            raise Exception("Input alphabet is not subset of tape alphabet")

        if self._blank_sym not in self._tape_alphabet:
            raise Exception("Blank symbol is not into the tape alphabet")

        if self._init_state not in self._states:
            raise Exception("Initial state is not a valid state")

        if not self._final_states.issubset(self._states):
            raise Exception("Final states are not a subset of states")

        for k, v in self._trans_function.items():
            if len(k) != 2 or len(v) != 3:
                raise Exception(
                    "Invalid format in transition %s -> %s" % (str(k), str(v))
                )

            inv_state = None
            if k[0] not in self._states:
                inv_state = k[0]
            if v[0] not in self._states:
                inv_state = v[0]
            if inv_state:
                raise Exception(
                    "Invalid state %s in transition %s -> %s"
                    % (str(inv_state), str(k), str(v))
                )

            inv_sym = None
            if k[1] not in self._tape_alphabet:
                inv_sym = k[1]
            if v[1] not in self._tape_alphabet:
                inv_sym = v[1]
            if inv_sym:
                raise Exception(
                    "Invalid symbol %s in transition %s -> %s"
                    % (str(inv_sym), str(k), str(v))
                )

            if v[2] not in movements:
                raise Exception(
                    "Invalid movement %s in transition %s -> %s"
                    % (str(v[2]), str(k), str(v))
                )

    def __str__(self):
        return (
            "States: %s\n"
            "Input alphabet: %s\n"
            "Tape alphabet: %s\n"
            "Blank symbol: %s\n"
            "Initial state: %s\n"
            "Final states: %s\n"
            "Halt state: %s\n\n"
            "Transition Function:\n%s"
            % (
                str(self._states),
                str(self._in_alphabet),
                str(self._tape_alphabet),
                str(self._blank_sym),
                str(self._init_state),
                str(self._final_states),
                str(self._halt_state),
                str(self._trans_function),
            )
        )


# Turing Machine Observers base class
##############################################################################


class BaseTuringMachineObserver(metaclass=ABCMeta):
    @abstractmethod
    def on_step_start(self, state, symbol):
        raise NotImplementedError()

    @abstractmethod
    def on_step_end(self, state, symbol, movement):
        raise NotImplementedError()

    @abstractmethod
    def on_tape_changed(self, head_pos):
        raise NotImplementedError()

    @abstractmethod
    def on_head_moved(self, head_pos, old_head_pos):
        raise NotImplementedError()
