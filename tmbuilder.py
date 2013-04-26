# -*- coding: utf-8 -*-

from tm import TuringMachine

class TuringMachineBuilder:
    """
    Creates a turing machine step by step by retrieving all the necessary 
    information.
    
    By default (can be specified) sets the halt state to 'HALT and the
    blank symbol to '#'
    """
    
    def __init__(self, haltstate='HALT', blank='#'):
        """
        Initialize a new TuringMachineBuilder with the specified haltstate and
        blank symbol.
        
        haltstate takes as default value 'HALT'
        blnak takes as default value '#'
        """
        self._states = set()
        self._in_alphabet = set()
        self._trans_function = {}
        self._istate = None
        self._fstates = set()
        self._blank = blank
        self._haltstate = haltstate
        
        # It can be added at the creation type becaus is treated as an iterable
        self._states.add(haltstate)
        
    #
    #    
    def addTransition(self, state, symbol, new_state, new_symbol, movement):
        """
        addTransition(state, symbol, new_state, new_symbol, movement)
                
        Adds the transition:
            From state,symbol To new_state writing new_symbol at the current 
            possition and moving the head in movement direction
             
        - state: something that represents a state, must be hashable
        - symbol: something that represents a symbol, must be hashable
        - new_state: something that represents a state, must be hashable
        - new_symbol: something that represents a symbol, must be hashable
        - movement: TuringMachine.MOVE_LEFT or TuringMachine.MOVE_RIGHT or 
                    TuringMachine.NON_MOVEMENT
        """
        
        if movement not in TuringMachine.HEAD_MOVEMENTS:        
            raise Exception('Invalid movement')
        
        if state not in self._states:
            self._states.add(state)
            
        if symbol != self._blank and symbol not in self._in_alphabet:
            self._in_alphabet.add(symbol)
            
        if new_state not in self._states:
            self._states.add(new_state)
            
        if new_symbol != self._blank and new_symbol not in self._in_alphabet:
            self._in_alphabet.add(new_symbol)
            
        self._trans_function[(state,symbol)] = (new_state, new_symbol,
                                                 movement)
    #
    #                                             
    def addFinalState(self, state):
        """
        Adds the specified state to the set of final states
        """
        if state not in self._states:
            self._states.add(state)
        if state not in self._fstates:
            self._fstates.add(state)
           
    #
    #      
    def setInitialState(self, state):
        """
        Set the specified state as the initial. Mandatory operation
        """
        if state not in self._states:
            self._states.add(state)
        self._istate = state
        
    #
    #
    def create(self):
        """
        Creates a turing machine instance with the collected information.
        
        If the initial state remains unset when this method is called, will
        raises an Exception.
        
        At this point the tape_alphabet is set to be: in_alphabet U {blank}
        """
        if self._istate == None:
            raise Exception('It is necessary to specify an initial state')
        
        
        tape_alphabet = set(self._in_alphabet)
        tape_alphabet.add(self._blank)
        
        return TuringMachine(self._states, self._in_alphabet, tape_alphabet,
                             self._trans_function, self._istate, 
                             self._fstates, self._haltstate, self._blank)
                             
    #
    #
    def getHaltState(self):
        """
        Returns the halt state specified or assigned by default on the 
        initialization of this Builder
        """
        return self._haltstate
            

if __name__ == '__main__':
    tmb = TuringMachineBuilder()
    
    tmb.addTransition(1, 0, 2, 1, TuringMachine.MOVE_RIGHT)
    tmb.addTransition(1, 1, 2, 0, TuringMachine.MOVE_RIGHT)
    tmb.addTransition(2, 0, 1, 0, TuringMachine.NON_MOVEMENT)
    tmb.addTransition(2, 1, 3, 1, TuringMachine.MOVE_RIGHT)
    tmb.addTransition(3, 0, 'HALT', 0, TuringMachine.NON_MOVEMENT)
    tmb.addTransition(3, 1, 'HALT', 1, TuringMachine.NON_MOVEMENT)
    tmb.addTransition(3, '#', 'HALT', '#', TuringMachine.NON_MOVEMENT)
    
    tmb.setInitialState(1)
    tmb.addFinalState(2)
    
    print tmb.create()
    

    