#!/usr/vin/env python
# -*- coding: utf-8 -*-

import os
import sys

import tm
import tmparser
import tmexceptions


from PyQt4 import QtGui, QtCore

__prog__='Universal Turing Machine Simulator'


#
#
def main():

    # Initialized the qt application    
    app = QtGui.QApplication(sys.argv)    
    gui = GUI()
    gui.initGUI()
    gui.installHandlers()    
    gui.show()    
    sys.exit(app.exec_())

#
#
class GUI(QtGui.QWidget):
    
    TAPE_SIZE = 29
    TAPE_HEAD = int(round(TAPE_SIZE / 2))
    DEF_WIDTH = 800
    DEF_HEIGHT = 600
    HSPACING = 15
    VSPACING = 10
    QCOLOR_RED = QtGui.QColor(255,0,0)
    QCOLOR_BLK = QtGui.QColor(0,0,0)
    
    #
    #
    def __init__(self):
        super(GUI, self).__init__()
        # Turing machine and Turing machine parser
        self.parser = tmparser.TuringMachineParser()
        self.turing_machine = None
        
    #
    #
    def initGUI(self):
        
        # Configure window
        self.setMinimumSize(GUI.DEF_WIDTH, GUI.DEF_HEIGHT)   
        #self.setMaximumSize(GUI.DEF_WIDTH, GUI.DEF_HEIGHT)
        self.setWindowTitle(__prog__)
        
        self.main_vbox = QtGui.QVBoxLayout(self)
        
        # Add Tape widgets
        self._initTape()        
        # Add log text box
        self._initLogArea()
        
        # Add controls
        self._initControlArea()
        
        self.resize(GUI.DEF_WIDTH, GUI.DEF_HEIGHT)
        
        
    #
    #
    def installHandlers(self):
        self.set_tm_btn.clicked.connect(self.onSetTuringMachineClicked)
        self.set_tape_btn.clicked.connect(self.onSetTapeClicked)
        self.run_step_btn.clicked.connect(self.onRunStepClicked)
        self.run_all_btn.clicked.connect(self.onRunUntilHaltClicked)  
        self.src_load_btn.clicked.connect(self.onLoadClicked)
        self.src_save_btn.clicked.connect(self.onSaveClicked)
        
        
    #
    # QtGui event handlers
    #
    
    #
    #
    def onSetTuringMachineClicked(self):
        
        tmstr = str(self.src_textbox.toPlainText())
        try:
            self.parser.clean()
            self.parser.parseString(tmstr)
            self.turing_machine = self.parser.create()
            self.turing_machine.attachObserver(self)
            
            self.log_textbox.setTextColor(GUI.QCOLOR_BLK)
            self.log_textbox.append('Turing machine set')
            self.log_textbox.append('Current state: ' + 
                                str(self.turing_machine.getCurrentState()))
        except Exception, e:
            self.log_textbox.setTextColor(GUI.QCOLOR_RED)
            self.log_textbox.append(str(e))
        except AssertionError, e:
            self.log_textbox.setTextColor(GUI.QCOLOR_RED)
            self.log_textbox.append(str(e))
            
    #
    #
    def onSetTapeClicked(self):
        tapestr = str(self.tape_textbox.toPlainText())
        if self.turing_machine != None:
            self.turing_machine.setTape(tapestr)
        else:
            self.log_textbox.setTextColor(GUI.QCOLOR_RED)
            self.log_textbox.append('Set the turing machine before set the tape')
            
    #
    #
    def onRunStepClicked(self):
        
        try:
            self.turing_machine.step()
            
        except tmexceptions.HaltStateException, e:
            self.log_textbox.setTextColor(GUI.QCOLOR_RED)
            self.log_textbox.append(str(e))
            
        except tmexceptions.UnsetTapeException, e:
            self.log_textbox.setTextColor(GUI.QCOLOR_RED)
            self.log_textbox.append(str(e))
            
        except tmexceptions.UnknownTransitionException, e:
            self.log_textbox.setTextColor(GUI.QCOLOR_RED)
            self.log_textbox.append(str(e))
            
    #
    #            
    def onRunUntilHaltClicked(self):
        
        if self.turing_machine.isAtHaltState():
            self.log_textbox.setTextColor(GUI.QCOLOR_RED)
            self.log_textbox.append('The current state is halt state')
            
        else:
            self.log_textbox.setTextColor(GUI.QCOLOR_BLK)
            self.log_textbox.append('---------- Run Until Halt ----------')
            
            try:
                while not self.turing_machine.isAtHaltState():
                    self.turing_machine.step()
                
            except tmexceptions.UnsetTapeException, e:
                self.log_textbox.setTextColor(GUI.QCOLOR_RED)
                self.log_textbox.append(str(e))
                
            except tmexceptions.UnknownTransitionException, e:
                self.log_textbox.setTextColor(GUI.QCOLOR_RED)
                self.log_textbox.append(str(e))
                
    #
    #
    def onLoadClicked(self):
        
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Load file',
                                                  os.path.expanduser('~'))
                                                  
        if fname:
            f = open(fname, 'r')
            fstr = f.read()
            self.src_textbox.setPlainText(fstr)
            f.close()
            # TODO add notification on log_textbox
            
    #
    #
    def onSaveClicked(self):
        
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file',
                                                  os.path.expanduser('~'))
                                                  
        if fname:
            f = open(fname, 'w')
            fstr = str(self.src_textbox.toPlainText())
            f.write(fstr)
            f.close()
    #
    # Turing Machine observer methods
    #

    #
    #
    def onStepStart(self, current_state, current_tape_symbol):
        pass
    
    #
    #
    def onStepEnd(self, new_state, writed_symbol, movement):
        self.log_textbox.setTextColor(GUI.QCOLOR_BLK)
        self.log_textbox.append('Writed Symbol: ' + str(writed_symbol) )
        
        if movement == tm.TuringMachine.MOVE_LEFT:            
            self.log_textbox.append('Head moved to the left')
        elif movement == tm.TuringMachine.MOVE_RIGHT:
            self.log_textbox.append('Head moved to the right')            
        else:
            self.log_textbox.append('Head remains at the same position')
        
        self.log_textbox.append('Current state: ' + str(new_state))
    
    #
    #
    def onTapeChanged(self, head_pos):
        self._redrawTape(head_pos)
    
    #
    #
    def onHeadMoved(self, head_pos, old_head_pos):
        self._redrawTape(head_pos)

        
    #
    # 'Private'
    #
    
    #
    # Creates and adds the tape widgets
    def _initTape(self):
        self.tape_label = QtGui.QLabel('Tape', self)   
        
        self.tape_hbox = QtGui.QHBoxLayout()
                
#        self.tape_lbutton = QtGui.QPushButton('<', self)
#        self.tape_rbutton = QtGui.QPushButton('>', self)        
        self.tape_textboxes = self._createTape()
        
        
#        self.tape_hbox.addWidget(self.tape_lbutton)
        for txbx in self.tape_textboxes:
            self.tape_hbox.addWidget(txbx)
#        self.tape_hbox.addWidget(self.tape_rbutton)
        
        
        self.main_vbox.addWidget(self.tape_label, 0, QtCore.Qt.AlignCenter)        
        self.main_vbox.addLayout(self.tape_hbox, 1)
        self.main_vbox.addSpacing(GUI.VSPACING)
        
        
    #
    #
    def _createTape(self):
        tptx = [QtGui.QLineEdit(self) for i in xrange(GUI.TAPE_SIZE)]
        for txbx in tptx:
            txbx.setReadOnly(True)
            txbx.setFocusPolicy(QtCore.Qt.NoFocus)
            txbx.setAlignment(QtCore.Qt.AlignHCenter)
        tptx[GUI.TAPE_HEAD].setStyleSheet("QLineEdit { border: 2px solid gray; }")
        return tptx
        
    #
    #
    def _initLogArea(self):
        self.log_textbox = QtGui.QTextEdit(self)
        self.log_textbox.setReadOnly(True)
        
        self.main_vbox.addWidget(self.log_textbox, 1)
        self.main_vbox.addSpacing(GUI.VSPACING)
        
    #
    #
    def _initControlArea(self):
        self.ctrl_hbox = QtGui.QHBoxLayout()
        
        # Add source text box and load/save buttons
        ctrl_llabel = QtGui.QLabel("TM Source Code", self)
        self.src_textbox = QtGui.QPlainTextEdit(self)
        self.src_load_btn = QtGui.QPushButton('Load', self)
        self.src_save_btn = QtGui.QPushButton('Save', self)
        
        self.ctrl_lvbox = QtGui.QVBoxLayout()
        self.ctrl_lvbox.addWidget(ctrl_llabel, 0, QtCore.Qt.AlignCenter)
        self.ctrl_lvbox.addWidget(self.src_textbox)
        self.ctrl_lvbox.addWidget(self.src_load_btn)
        self.ctrl_lvbox.addWidget(self.src_save_btn)
        
        # Add control buttons
        ctrl_rlabel = QtGui.QLabel("Tape's Initial Value", self)
        self.tape_textbox = QtGui.QPlainTextEdit(self)
        self.set_tm_btn = QtGui.QPushButton('Set TM', self)
        self.set_tape_btn = QtGui.QPushButton('Set Tape', self)
        self.run_step_btn = QtGui.QPushButton('Run Step', self)
        self.run_all_btn = QtGui.QPushButton('Run Until Halt', self)
        
        self.ctrl_rvbox = QtGui.QVBoxLayout()
        self.ctrl_rvbox.addWidget(ctrl_rlabel, 0, QtCore.Qt.AlignCenter)
        self.ctrl_rvbox.addWidget(self.tape_textbox)
        self.ctrl_rvbox.addWidget(self.set_tm_btn)
        self.ctrl_rvbox.addWidget(self.set_tape_btn)
        self.ctrl_rvbox.addWidget(self.run_step_btn)
        self.ctrl_rvbox.addWidget(self.run_all_btn)   
       
        # Add the control area to the main layout
        self.ctrl_hbox.addLayout(self.ctrl_lvbox, 2)
        self.ctrl_hbox.addSpacing(GUI.HSPACING)
        self.ctrl_hbox.addLayout(self.ctrl_rvbox, 1)
        self.main_vbox.addLayout(self.ctrl_hbox, 4)
        
    #
    #
    def _redrawTape(self, head_pos):
        sym = self.turing_machine.getSymbolAt(head_pos)
        self.tape_textboxes[GUI.TAPE_HEAD].setText(str(sym))
        
        for i in xrange(1, GUI.TAPE_HEAD + 1):
            txtbx_index = GUI.TAPE_HEAD - i
            tape_index = head_pos - i
            self.tape_textboxes[txtbx_index].setText(
                            str(self.turing_machine.getSymbolAt(tape_index)) )
                                
        for inc, i in enumerate(xrange(GUI.TAPE_HEAD + 1, GUI.TAPE_SIZE)):
            tape_index = head_pos + inc + 1
            self.tape_textboxes[i].setText(
                            str(self.turing_machine.getSymbolAt(tape_index)) )
#
#
if __name__ == '__main__':    
    main()