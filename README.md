Universal Turing Machine
========================
_Simple Turing Machine simulator implemented using Python and PyQt4_

![application logo][logo]

## Executing the simulator ##

To execute the simulator has to be executed the utm.py file.

  + In any O.S with a python interpreter
    - python utm.py
  + In linux giving execution permissions to utm.py
    - ./utm.py

## Requirements ##

  - Python 2.7
  - PyQt4
    - Fedora: **yum install PyQt4**
    - Ubuntu: **apt-get install python-qt4**

## Simulator language and Parser ##

It is possible to write the source code directly on the simulator interface or write
it in an external editor and load it later.

In order to simplify the syntax, any symbol or state defined in the machine instructions
is automatically added to the set of possible symbols or states of the turing machine.

### Syntax ###

  + Comments: Lines beginning with '%' are ignored by the parser. 

  + It is mandatory to specify a HALT state and an INITIAL state, by using the following syntax
    + **HALT _\<state\>_**
    + **INITIAL _\<state\>_**

   Where *\<state\>* is any text you want without spaces. It is not possible to specify more than one HALT/INITIAL state.

  + Optionally an state can be marked as a final state with the syntax:
    + **FINAL _\<state\>_**
  
  + To go from one state to an other is necessary to specify the proper transitions to do that.
    Transitions must be specified as follows.
    + *\<from_state\>*, *\<symbol_on_tape\>* **->** *\<to_state\>*, *\<symbol_to_write\>*, *\<head_movement\>*
      + *\<from_state\>* and *\<to_state\>* can be any text you want without spaces.
      + *\<symbol_on_tape\>* and *\<symbol_to_write\>* can be any character (one character!) you want.
      + *\<head_movement\>* must be one of the following characters:
  
        + '<' -- Move to the left
        + '>' -- Move to the right
        + '_' -- No movement

Here there are some syntax examples [Examples][examples]

[logo]: ./graphics/icon.png "Application Logo"
[examples]: ./tm_examples
