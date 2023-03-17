Universal Turing Machine
========================
_Simple Turing Machine simulator implemented using Python and PySide2_

![application logo][logo]

## Requirements ##

  - [Pipx](https://pypa.github.io/pipx/installation/) (recommended)
  - [Hatch](https://hatch.pypa.io/latest/install/)
    - `pipx install hatch`

All dependencies are manged by hatch, once you have it installed just
open a terminal on the *root* of the project and run `hatch shell`. This
will sync all dependencies and activate hatch's default python environment.

## Executing the simulator ##

Provided that you are using *hatch*, once your terminal is "inside"
`hatch shell`, just type the following command (with the terminal working
directory on the root of the project.)

```shell
python -m utm
```

## Simulator language and Parser ##

It is possible to write the source code directly on the simulator interface or 
write it in an external editor and load it later. For the sake of simplicity, 
any symbol or state defined in the machine instructions is automatically
added to the set of possible symbols or states of the turing machine.

### Syntax ###

  + Comments: Lines beginning with '%' are ignored by the parser. 

  + It is mandatory to specify HALT and INITIAL states, by using the
    following syntax:

    + **HALT _\<state\>_**
    + **INITIAL _\<state\>_**

    Where *\<state\>* is any text you want without spaces, non-blank UTF-8 characters are also supported, i.e., emojis.

  + Optionally an state can be marked as a final state with the syntax:
    + **FINAL _\<state\>_**
  
  + To go from one state to another is necessary to specify the proper 
    transitions using the following syntax:
    
    + *\<from_state\>*, *\<symbol_on_tape\>* **->** *\<to_state\>*, *\<symbol_to_write\>*, *\<head_movement\>*
      + *\<from_state\>* and *\<to_state\>* can be any text you want without spaces.
      + *\<symbol_on_tape\>* and *\<symbol_to_write\>* must be exactly one
        character.
      + *\<head_movement\>* must be one of the following characters:
  
        + '<' -- Move to the left
        + '>' -- Move to the right
        + '_' -- No movement

Here there are some syntax examples [Examples][examples]

[logo]: ./graphics/icon.png "Application Logo"
[examples]: ./tm_examples
