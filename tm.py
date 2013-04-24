#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import tmexceptions


class TuringMachine:
    """
    Represents a turing machine, to work propertly there are some restrictions:
        - symbols on input alphabet and tape alphabet must be one char length

        - transition function must be a dictionary with the following format:
                        (state, symbol) : (state, symbol, movement)

        - movements are defined by the following symbols:
            - L : left
            - R : right
            - N : Non move
    """

    MOVE_RIGHT = 'R'
    MOVE_LEFT = 'L'
    NON_MOVEMENT = 'N'

    #
    #
    def __init__(self, states, in_alphabet, tape_alphabet, trans_function,
                 istate, fstates, hstate, blank):
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
                Halt state. If reached, execution stops inmediatly
            - blank: 
                Default symbol in all unespecified tape possitions
        """
        self.states = frozenset(states);
        self.in_alphabet = frozenset(in_alphabet)
        self.tape_alphabet = frozenset(tape_alphabet)
        self.trans_function = copy.copy(trans_function)
        self.istate = istate
        self.fstates = frozenset(fstates)
        self.hstate = hstate
        self.blank = blank

        self._checkData()

        self.tape = None
        self.head = 0
        self.cur_state = istate

    #
    #
    def step(self):
        """
        Performs one execution step.
            
            - If it's at Halt state raises HaltStateException
            - If tape is unset raises UnsetTapeException
        """
        if self.isAtHaltState():
            raise tmexceptions.HaltStateException('Current state is halt state')
        if self.tape == None:
            raise tmexceptions.UnsetTapeException(
                'Tape must be set before perform an step')
                
        cur = (self.cur_state, self.tape[self.head])
        try:
            state, sym, movement = self.trans_function[cur]
            
            self.tape[self.head] = sym
            self.cur_state = state
            
            if movement == TuringMachine.MOVE_LEFT:
                if self.head == 0:
                    self.tape.insert(0, self.blank)
                    
            elif movement == TuringMachine.MOVE_RIGHT:
                self.head += 1
                if self.head == len(self.tape):
                    self.tape.append(self.blank)                
            
        except KeyError:
            raise tmexceptions.UnknownTransitionException(
                'There are no transition for %s' % str(cur))

    #
    #
    def getCurrentState(self):
        """
        Returns the current state (Cpt. Obvious)
        """
        return self.cur_state

    #
    #
    def setTape(self, tape, head_pos=0):
        """
        setTape(tape:[], head_pos:int)

        Set tape and head position

        Head position takes as default value 0
        If head position is negative or greater than tape length the tape is
        filled with blanks
        
        If tape contains an invalid symbol raises an InvalidSymbolException
        """
        
        for s in tape:
            if s not in self.tape_alphabet:
                raise tmexceptions.InvalidSymbolException(
                    'Invalid tape symbol %s' % str(s))
        
        # If head pos is out of tape make tape grow with blanks 
        if head_pos < 0:
            self.tape = [self.blank] * (-head_pos)
            self.tape.extend(tape)
            self.head = 0
        elif head_pos >= len(tape):
            self.tape = list(tape)
            self.tape.extend( [self.blank] * (head_pos - len(tape)) )
            self.head = head_pos
        else:
            self.tape = list(tape)
            self.head = head_pos

    #
    #
    def isAtHaltState(self):
        """
        Returns true only if current state is the halt state
        """
        return self.curr_state == self.hstate

    #
    #
    def isTapeSet(self):
        """
        Returns true only if tape is set        
        """
        return self.tape != None

    #
    #
    def _checkData(self):
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
        movements = frozenset([TuringMachine.MOVE_LEFT, 
                                TuringMachine.MOVE_RIGHT,
                                TuringMachine.NON_MOVEMENT])


        if not self.in_alphabet.issubset(self.tape_alphabet):
            raise Exception('Input alphabet is not subset of tape alphabet')

        if blank not in self.tape_alphabet:
            raise Exception('Blank symbol is not into the tape alphabet')

        if self.istate not in self.states:
            raise Exception('Initial state is not a valid state')

        if not self.fstates.issubset(self.states):
            raise Exception('Final states are not a subset of states')

        for k, v in self.trans_function.iteritems():
            if len(k) != 2 or len(v) != 3: 
                raise Exception('Invalid format in transition %s -> %s' %
                                (str(k), str(v)))

            inv_state = None
            if k[0] not in self.states:    inv_state = k[0]
            if v[0] not in self.states:    inv_state = v[0]
            if inv_state:
                raise Exception('Invalid state %s in transition %s -> %s' %
                                (str(inv_state), str(k), str(v)))
                
            inv_sym = None
            if k[1] not in self.tape_alphabet: inv_sym = k[1]
            if v[1] not in self.tape_alphabet: inv_sym = v[1]
            if inv_sym:
                raise Exception('Invalid symbol %s in transition %s -> %s' %
                                (str(inv_sym), str(k), str(v)))

            if v[2].upper() not in movements:
                raise Exception('Invalid movement %s in transition %s -> %s' %
                                (str(v[2]), str(k), str(v)))

    #
    #
    def __str__(self):
        return    'States: %s\n' \
                'Input alphabet: %s\n' \
                'Tape alphabet: %s\n' \
                'Blank symbol: %s\n' \
                'Initial state: %s\n' \
                'Final states: %s\n' \
                'Halt state: %s\n\n' \
                'Transition Function:\n%s' \
                 % (
                    str(self.states), str(self.in_alphabet), 
                    str(self.tape_alphabet), str(self.blank), str(self.istate),
                    str(self.fstates), str(self.hstate), 
                    str(self.trans_function)
                    )


# Test class
if __name__ == '__main__':

    hstate = 'H'
    states = set([1,2, hstate])
    in_alphabet = set(['0','1'])
    tape_alphabet = set(['0','1','#'])
    istate = 1
    fstates = set([2])
    blank = '#'
    trans_function = {
                    (1,'0'): (2,'1', 'R'),
                    (1,'1'): (2,'0', 'R'),
                    (2,'0'): (1,'0', 'L'),
                    (2,'1'): (3,'1', 'R'),
                    (3,'0'): (hstate,'0', 'N'),
                    (3,'1'): (hstate,'1', 'N'),
                    (3,blank): (hstate,blank,'N')
                }


    try:
        tm = TuringMachine(states, in_alphabet, tape_alphabet, trans_function,
                        istate, fstates, hstate, blank)
    except Exception as e:
        print 'Error:', e

    print 'Adding state 3 to the machine states'
    states.add(3)

    tm = TuringMachine(states, in_alphabet, tape_alphabet, trans_function,
                        istate, fstates, hstate, blank)

    print 'Turing Machine'
    print tm