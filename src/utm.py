#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pkgutil
import sys

import highlighters
from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from tm import BaseTuringMachineObserver, TuringMachine, TuringMachineParser
from tm.exceptions import UnknownTransitionException, HaltStateException, \
                          TapeNotSetException

__program__ = 'Universal Turing Machine Simulator'
__version__ = '1.1'

__author__ = "Josep Pon Farreny"
__copyright__ = "Copyright 2012-2016, Josep Pon Farreny"

__maintainer__ = "Josep Pon Farreny"
__email__ = "jponfarreny@diei.udl.cat"
__status__ = "Development"


# UTM Main
##############################################################################

def main():

    # Initialized the qt application    
    app = QtGui.QApplication(sys.argv)    
    gui = GUI()
    gui.init_gui()
    gui.show()
    sys.exit(app.exec_())


# UTM Qt GUI
##############################################################################


class GUI(QtGui.QWidget):
    
    TAPE_SIZE = 31
    TAPE_HEAD = TAPE_SIZE // 2
    TAPE_HEAD_LEFT = TAPE_HEAD - 1
    TAPE_HEAD_RIGHT = TAPE_HEAD + 1
    DEF_WIDTH = 800
    DEF_HEIGHT = 600
    H_SPACING = 10
    V_SPACING = 5

    # Tape style(s)
    TAPE_HEAD_STYLE = 'QLineEdit { border: 2px solid red; background: white;}'

    def __init__(self):
        super().__init__()

        self.parser = TuringMachineParser()
        self.turing_machine = None

    def init_gui(self):
        # Configure window
        self.setMinimumSize(GUI.DEF_WIDTH, GUI.DEF_HEIGHT)   
        self.setWindowTitle(__program__)

        self.main_vbox = QtGui.QVBoxLayout(self)

        # Set GUI icon
        self._init_icon()
        # Add Tape widgets
        self._init_tape()
        # Add log text box
        self._init_log_area()
        # Add controls
        self._init_control_area()
        # Install handlers
        self._install_handlers()
        
        self.resize(GUI.DEF_WIDTH, GUI.DEF_HEIGHT)

    def redraw_tape(self, head_pos):
        blank = self.turing_machine.get_blank_symbol()

        # sym = self.turing_machine.getSymbolAt(head_pos)
        # self.tape_textboxes[GUI.TAPE_HEAD].setText(
        #    '' if sym == blank else str(sym))

        for i in range(GUI.TAPE_HEAD + 1):
            txt_box_index = GUI.TAPE_HEAD - i
            tape_index = head_pos - i
            sym = self.turing_machine.get_symbol_at(tape_index)
            self.tape_textboxes[txt_box_index].setText(
                '' if sym == blank else str(sym))

        for inc, i in enumerate(range(GUI.TAPE_HEAD + 1, GUI.TAPE_SIZE)):
            tape_index = head_pos + inc + 1
            sym = self.turing_machine.get_symbol_at(tape_index)
            self.tape_textboxes[i].setText('' if sym == blank else str(sym))

    def print_error_log(self, error):
        """Prints a message on the log_textbox
        Text Color: RED
        """
        self.log_textbox.setTextColor(Qt.red)
        self.log_textbox.setFontWeight(QtGui.QFont.Normal)
        self.log_textbox.append(error)

    def print_info_log(self, msg):
        """Prints a message on the log_textbox
        Text Color: BLACK
        """
        self.log_textbox.setTextColor(Qt.black)
        self.log_textbox.setFontWeight(QtGui.QFont.Normal)
        self.log_textbox.append(msg)

    def print_striking_info_log(self, msg):
        """Prints a message on the log_textbox making it more visible than a
        normal log
        """
        self.log_textbox.setTextColor(Qt.darkBlue)
        self.log_textbox.setFontWeight(QtGui.QFont.Bold)
        self.log_textbox.append(msg)

    #
    # QtGui event handlers
    #

    def on_set_turing_machine_clicked(self):
        tm_str = str(self.src_textbox.toPlainText())
        try:
            self.parser.clean()
            self.parser.parseString(tm_str)
            self.turing_machine = self.parser.create()
            self.turing_machine.attach_observer(TuringMachineObserver(self))
            
            self.print_info_log('Turing machine created')
            self.print_info_log('Current state: ' +
                                str(self.turing_machine.get_current_state()))
                                
        except Exception as e:
            self.print_error_log('Error: %s' % str(e))

    def on_set_tape_clicked(self):
        tape_str = str(self.tape_textbox.toPlainText())
        if self.turing_machine is not None:
            self.turing_machine.set_tape(tape_str)
            self.turing_machine.set_at_initial_state()
            self.print_info_log('Tape value established')
        else:
            self.print_error_log("Error: The Turing machine must be set"
                                 " before setting the tape")

    def on_run_step_clicked(self):
        try:
            self.turing_machine.run_step()
        except HaltStateException as e:
            self.print_error_log(str(e))
        except TapeNotSetException as e:
            self.print_error_log(str(e))
        except UnknownTransitionException as e:
            self.print_error_log(str(e))
        except AttributeError:
            self.print_error_log('Error: Turing machine is unset')
        except Exception as e:
            self.print_error_log(str(type(e)))

    def on_run_until_halt_clicked(self):
        try:
            if self.turing_machine.is_at_halt_state():
                self.print_error_log('Error: The Turing Machine is on halt state')
            else:
                self.print_info_log('---------- Run Until Halt ----------')
                
                try:
                    while not self.turing_machine.is_at_halt_state():
                        self.turing_machine.run_step()
                except TapeNotSetException as e:
                    self.print_error_log(str(e))
                except UnknownTransitionException as e:
                    self.print_error_log(str(e))
        except AttributeError:
            self.print_error_log('Error: Turing machine is unset')

    def on_load_clicked(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Load file',
                                                  os.path.expanduser('~'))
        if fname:
            f = open(fname, 'r')
            fstr = f.read()
            self.src_textbox.setPlainText(fstr)
            f.close()
            
            self.print_info_log('Loaded file: %s' % fname)

    def on_save_clicked(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file',
                                                  os.path.expanduser('~'))
        if fname:
            f = open(fname, 'w')
            fstr = str(self.src_textbox.toPlainText())
            f.write(fstr)
            f.close()
            self.print_info_log('Saved file: %s' % fname)

    def on_clear_log_clicked(self):
    
        self.log_textbox.clear()

    def on_print_all_tape(self):
        if self.turing_machine:
            try:
                tape_value = ' '.join(self.turing_machine.get_tape_iterator())
                self.print_info_log('***************************************')
                self.print_info_log('Tape Values:')
                self.print_striking_info_log(tape_value)
                self.print_info_log('***************************************')
            except Exception as e:
                self.print_error_log(str(e))
        else:
            self.print_error_log("Error: The Turing Machine must be set"
                                 " before printing the tape")

    #
    # 'Private'
    #

    def _init_icon(self):
        data = pkgutil.get_data('resources', 'icon.png')
        pix_map = QtGui.QPixmap()
        pix_map.loadFromData(data)
        self.setWindowIcon(QtGui.QIcon(pix_map))

    def _init_tape(self):
        self.tape_label = QtGui.QLabel('Tape', self)
        self.tape_hbox = QtGui.QHBoxLayout()
                
        # self.tape_lbutton = QtGui.QPushButton('<', self)
        # self.tape_rbutton = QtGui.QPushButton('>', self)
        self.tape_textboxes = self._create_tape()

        # self.tape_hbox.addWidget(self.tape_lbutton)
        for txt_box in self.tape_textboxes:
            self.tape_hbox.addWidget(txt_box)
        # self.tape_hbox.addWidget(self.tape_rbutton)

        self.main_vbox.addWidget(self.tape_label, 0, Qt.AlignCenter)        
        self.main_vbox.addLayout(self.tape_hbox, 1)
        self.main_vbox.addSpacing(GUI.V_SPACING)

    def _create_tape(self):
        tape_txt_boxes = [QtGui.QLineEdit(self) for _ in range(GUI.TAPE_SIZE)]
        for txt_box in tape_txt_boxes:
            txt_box.setReadOnly(True)
            txt_box.setFocusPolicy(Qt.NoFocus)
            txt_box.setAlignment(Qt.AlignHCenter)
            
        tape_txt_boxes[GUI.TAPE_HEAD].setStyleSheet(GUI.TAPE_HEAD_STYLE)
        return tape_txt_boxes

    def _init_log_area(self):
        
        log_vbox = QtGui.QVBoxLayout()
                
        # Add log text box
        log_label = QtGui.QLabel('Activity Log', self)
        self.log_textbox = QtGui.QTextEdit(self)
        self.log_textbox.setReadOnly(True)
        log_vbox.addWidget(log_label, 0, Qt.AlignCenter)
        log_vbox.addWidget(self.log_textbox)
        
        # Add some control buttons
        log_hbox = QtGui.QHBoxLayout() 
        self.clear_log_btn = QtGui.QPushButton('Clear Log', self)
        self.print_all_tape_btn = QtGui.QPushButton('Print All Tape', self)

        log_hbox.addWidget(self.print_all_tape_btn)        
        log_hbox.addWidget(self.clear_log_btn)
        
        log_vbox.addLayout(log_hbox)        
        
        # Add all the previous stuff to the window layout
        self.main_vbox.addLayout(log_vbox, 1)
        self.main_vbox.addSpacing(GUI.V_SPACING)

    def _init_control_area(self):
        self.ctrl_hbox = QtGui.QHBoxLayout()
        
        # Add source text box and load/save buttons
        ctrl_llabel = QtGui.QLabel("TM Source Code", self)
        self.src_textbox = QtGui.QTextEdit(self)
        highlighters.TMSourceHighlighter(self.src_textbox)
        self.src_load_btn = QtGui.QPushButton('Load', self)
        self.src_save_btn = QtGui.QPushButton('Save', self)
        
        self.ctrl_lvbox = QtGui.QVBoxLayout()
        self.ctrl_lvbox.addWidget(ctrl_llabel, 0, Qt.AlignCenter)
        self.ctrl_lvbox.addWidget(self.src_textbox)
        ctrl_btn_hbox = QtGui.QHBoxLayout()
        ctrl_btn_hbox.addWidget(self.src_load_btn)
        ctrl_btn_hbox.addWidget(self.src_save_btn)
        self.ctrl_lvbox.addLayout(ctrl_btn_hbox)
        
        # Add control buttons
        ctrl_rlabel = QtGui.QLabel("Tape's Initial Value", self)
        self.tape_textbox = QtGui.QPlainTextEdit(self)
        self.set_tm_btn = QtGui.QPushButton('Set TM', self)
        self.set_tape_btn = QtGui.QPushButton('Set Tape', self)
        self.run_step_btn = QtGui.QPushButton('Run Step', self)
        self.run_all_btn = QtGui.QPushButton('Run Until Halt', self)
        
        self.ctrl_rvbox = QtGui.QVBoxLayout()
        self.ctrl_rvbox.addWidget(ctrl_rlabel, 0, Qt.AlignCenter)
        self.ctrl_rvbox.addWidget(self.tape_textbox)
        self.ctrl_rvbox.addWidget(self.set_tm_btn)
        self.ctrl_rvbox.addWidget(self.set_tape_btn)
        self.ctrl_rvbox.addWidget(self.run_step_btn)
        self.ctrl_rvbox.addWidget(self.run_all_btn)
        
        # Add some tooltips
        self.set_tape_btn.setToolTip('Sets the tape values and forces the TM '
                                     'to be at the initial state')
       
        # Add the control area to the main layout
        self.ctrl_hbox.addLayout(self.ctrl_lvbox, 2)
        self.ctrl_hbox.addSpacing(GUI.H_SPACING)
        self.ctrl_hbox.addLayout(self.ctrl_rvbox, 1)
        self.main_vbox.addLayout(self.ctrl_hbox, 2)

    def _install_handlers(self):
        self.set_tm_btn.clicked.connect(self.on_set_turing_machine_clicked)
        self.set_tape_btn.clicked.connect(self.on_set_tape_clicked)
        self.run_step_btn.clicked.connect(self.on_run_step_clicked)
        self.run_all_btn.clicked.connect(self.on_run_until_halt_clicked)
        self.src_load_btn.clicked.connect(self.on_load_clicked)
        self.src_save_btn.clicked.connect(self.on_save_clicked)
        self.clear_log_btn.clicked.connect(self.on_clear_log_clicked)
        self.print_all_tape_btn.clicked.connect(self.on_print_all_tape)


class TuringMachineObserver(BaseTuringMachineObserver):

    def __init__(self, gui):
        self.gui = gui

    def on_step_start(self, current_state, current_tape_symbol):
        self.gui.print_info_log('+++++++++++++++++++++++++++++++++++++++++++++++')
        self.gui.print_info_log('Started step at state "%s" with tape symbol "%s"'
                                % (str(current_state), str(current_tape_symbol)))

    def on_step_end(self, new_state, writen_symbol, movement):
        self.gui.print_info_log('-----------------------------------------------')

        self.gui.print_info_log('Writen Symbol: ' + str(writen_symbol))

        if movement == TuringMachine.MOVE_LEFT:
            self.gui.print_info_log('Head moved to the left')
        elif movement == TuringMachine.MOVE_RIGHT:
            self.gui.print_info_log('Head moved to the right')
        else:
            self.gui.print_info_log('Head remains at the same position')

        self.gui.print_info_log('Current state: ' + str(new_state) +
                                (' (FINAL)' if self.gui.turing_machine.is_at_final_state() else ''))

    def on_tape_changed(self, head_pos):
        self.gui.redraw_tape(head_pos)

    def on_head_moved(self, head_pos, _):
        self.gui.redraw_tape(head_pos)


if __name__ == '__main__':    
    main()
