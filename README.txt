Universal Turing Machine
========================

To execute the program you can chose one of the following options:

    1- Open a terminal on the source code directory and execute it with:
        $ python utm.py

    2- Give execution permissions to the main file and then execute it as a 
	   binary file:

        $ chmod +x utm.py
        $ ./utm.py

    3- Give execution permissions to the utm.py file and then double click on it:

        $ chmod +x utm.py

		Now you can "double click" on the utm.py file and if the file manager
		asks what to do: Display, Run in Terminal, Run, Cancel ... Chose Run


*************************************************
HOW TO PROGRAM A TURING MACHINE FOR THE SIMULATOR
*************************************************

It is possible to write the source directly on the simulator interface or write 
it on an external editor and then load it using the "Load" button.

How are the symbols and states defined?

	The system will add it to the list of possible symbols/states when it finds
	them on the code.


--- Syntax ---

+ The comments are specified by writing an '%'' at the begining of the line.
  It is also possible to add any amount of white spaces before the '%'' symbol.
  E.g:

    % Comment 1
        % white spaces before the comment

    
+ It is mandatory to specify a HALT state and an INITIAL state, to do it you 
  have to use the following instructions:

    HALT <state>
    INITIAL <state>

  Where <state> is any text you want without spaces, e.g:

	% Whenever the TM finds the H state it will stop
	HALT H

	% The first state of the TM will be '1', so make sure to add transitions from
	% this state to another
	INITIAL 1

  It is not possible to specify more than one HALT/INITIAL state.


+ Optionally you can mark an state as a final state with the following instruction:

    % Marks the state '3' as final
    FINAL 3

  When the TM is on a final state, it is indicated on the log textbox.


+ The transitions are specified using the following syntax:

    <from_state>, <symbol_on_tape> -> <to_state>, <symbol_to_write>, <head_movement>

  <from_state> and <to_state> can be any text you want without spaces

  <symbol_on_tape> and <symbol_to_write> can be any character (only one) you want 

  <head_movement> must be one of the following characters:

    '<' - Move to the left
    '>' - Move to the right
    '_' - Don't move


  For example:

    1, a -> 3, b, >

    When the machine is at the state '1' and on the head position there is the 
    symbol 'a'. The machine will change the symbol 'a' to 'b', its new state
    will be '3' and the head will move one position to the right.