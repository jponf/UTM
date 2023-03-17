# -*- coding: utf-8 -*-

from utm.tm import TuringMachine


class TuringMachineBuilder:
    """Incremental creation of a turing machine."""

    def __init__(self):
        """Initialize a new TuringMachineBuilder."""
        self._states = set()
        self._in_alphabet = set()
        self._trans_function = {}
        self._init_state = None
        self._final_states = set()

        self._blank = None
        self._halt_state = None

    def clean(self):
        """Clear all the previous stored data."""
        self._states = set()
        self._in_alphabet = set()
        self._trans_function = {}
        self._init_state = None
        self._final_states = set()

        self._blank = None
        self._halt_state = None

    def add_transition(self, state, symbol, new_state, new_symbol, movement):
        """Adds the transition.

        :param state: State from which the transition starts.
        :param symbol: Symbol that triggers the transition.
        :param new_state: Machine's state after the transition.
        :param new_symbol: Symbol to write on the tape.
        :param movement: Direction in which the tape has to be moved.

        :raise Exception: if symbols are longer than one character.
        """
        if movement not in TuringMachine.HEAD_MOVEMENTS:
            raise Exception("Invalid movement")

        if (hasattr(symbol, "len") and len(symbol) > 1) or (
            hasattr(new_symbol, "len") and len(new_symbol) > 1
        ):
            raise Exception("Symbol length > 1")

        if state not in self._states:
            self._states.add(state)

        if symbol != self._blank and symbol not in self._in_alphabet:
            self._in_alphabet.add(symbol)

        if new_state not in self._states:
            self._states.add(new_state)

        if new_symbol != self._blank and new_symbol not in self._in_alphabet:
            self._in_alphabet.add(new_symbol)

        self._trans_function[(state, symbol)] = (new_state, new_symbol, movement)

    def add_final_state(self, state):
        """Adds the give state to the set of final states."""
        if state not in self._states:
            self._states.add(state)
        if state not in self._final_states:
            self._final_states.add(state)

    def set_initial_state(self, state):
        """Sets the given state as the initial."""
        if state not in self._states:
            self._states.add(state)
        self._init_state = state

    def has_initial_state(self):
        """Tests if the initial state has been set.

        :return: True if it has been set, False otherwise.
        """
        return self._init_state is not None

    def has_halt_state(self):
        """Tests if the halt state has been set.

        :return: True if it has been set, False otherwise.
        """
        return self._halt_state is not None

    def has_blank_symbol(self):
        """Tests if the blank symbol has been set.

        :return: True if it has been set, False otherwise.
        """
        return self._blank is not None

    def set_blank_symbol(self, blank_sym):
        """Sets the blank symbol."""
        if not blank_sym or len(blank_sym) > 1:
            raise Exception("Symbol must be one char length")

        self._blank = blank_sym

    def set_halt_state(self, halt_state):
        """Sets the halt state."""
        # If there is a previous halt state. Check if it appears in some
        # transition otherwise delete it from the list of states
        if self.has_halt_state():
            old_remains = False
            for k, v in self._trans_function.items():
                if k[0] == self._halt_state or v[0] == self._halt_state:
                    old_remains = True
                    break

            if not old_remains:
                self._states.remove(self._halt_state)

        self._halt_state = halt_state
        self._states.add(self._halt_state)

    def create(self):
        """Creates a new turing machine instance using the previously set data

        The input alphabet is automatically set from the specified transitions
        plus the blank symbol.

        :raise Exception: If necessary elements are not set.
        """
        if not self.has_initial_state():
            raise Exception("It is necessary to specify an initial state")

        if not self.has_blank_symbol():
            raise Exception("It is necessary to specify the blank symbol")

        if not self.has_halt_state():
            raise Exception("It is necessary to specify the halt state")

        tape_alphabet = set(self._in_alphabet)
        tape_alphabet.add(self._blank)

        return TuringMachine(
            self._states,
            self._in_alphabet,
            tape_alphabet,
            self._trans_function,
            self._init_state,
            self._final_states,
            self._halt_state,
            self._blank,
        )

    def get_halt_state(self):
        return self._halt_state


if __name__ == "__main__":
    tmb = TuringMachineBuilder()

    tmb.set_blank_symbol("#")
    tmb.set_halt_state("HALT")

    tmb.add_transition(1, 0, 2, 1, TuringMachine.MOVE_RIGHT)
    tmb.add_transition(1, 1, 2, 0, TuringMachine.MOVE_RIGHT)
    tmb.add_transition(2, 0, 1, 0, TuringMachine.NON_MOVEMENT)
    tmb.add_transition(2, 1, 3, 1, TuringMachine.MOVE_RIGHT)
    tmb.add_transition(3, 0, "HALT", 0, TuringMachine.NON_MOVEMENT)
    tmb.add_transition(3, 1, "HALT", 1, TuringMachine.NON_MOVEMENT)
    tmb.add_transition(3, "#", "HALT", "#", TuringMachine.NON_MOVEMENT)

    tmb.set_initial_state(1)
    tmb.add_final_state(2)

    print(tmb.create())
