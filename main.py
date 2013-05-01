#!/usr/vin/env python
# -*- coding: utf-8 -*-

import sys
import tmparser

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
        tapestr = str(self.src_textbox.toPlainText())
        if self.turing_machine != None:
            self.turing_machine.setTape(tapestr)
            
    #
    #
    #def redrawTape(self, headpos):
        
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
        pass
    
    #
    #
    def onTapeChanged(self, head_pos):
        pass
    
    #
    #
    def onHeadMoved(self, head_pos, old_head_pos):
        pass

        
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
        self.src_textbox = QtGui.QPlainTextEdit(self)
        self.src_load_btn = QtGui.QPushButton('Load', self)
        self.src_save_btn = QtGui.QPushButton('Save', self)
        
        self.ctrl_lvbox = QtGui.QVBoxLayout()
        self.ctrl_lvbox.addWidget(self.src_textbox)
        self.ctrl_lvbox.addWidget(self.src_load_btn)
        self.ctrl_lvbox.addWidget(self.src_save_btn)
        
        # Add control buttons
        self.tape_textbox = QtGui.QPlainTextEdit(self)
        self.set_tm_btn = QtGui.QPushButton('Set TM', self)
        self.set_tape_btn = QtGui.QPushButton('Set Tape', self)
        self.run_step_btn = QtGui.QPushButton('Run Step', self)
        self.run_all_btn = QtGui.QPushButton('Run Until Halt', self)
        
        self.ctrl_rvbox = QtGui.QVBoxLayout()
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
if __name__ == '__main__':    
    main()