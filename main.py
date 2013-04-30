#!/usr/vin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui

__prog__='Universal Turing Machine Simulator'

#
#
def main():

    # Initialized the qt application    
    app = QtGui.QApplication(sys.argv)    
    gui = GUI()
    gui.initGUI()
    gui.show()
    sys.exit(app.exec_())
    
    
#
#
class GUI(QtGui.QWidget):
    
    TAPE_SIZE = 15    
    DEF_WIDTH = 800
    DEF_HEIGHT = 600
    
    #
    #
    def __init__(self):
        super(GUI, self).__init__()
        
    #
    #
    def initGUI(self):
        
        # Configure window
        self.setMinimumSize(GUI.DEF_WIDTH, GUI.DEF_HEIGHT)   
        self.setMaximumSize(GUI.DEF_WIDTH, GUI.DEF_HEIGHT)
        self.setWindowTitle(__prog__)
        
        # Add source text box
        self.src_textbox = QtGui.QPlainTextEdit(self)
        self.log_textbox = QtGui.QTextEdit(self)
        self.tape_textboxes = self._createTape()
        
        self.tape_left_button = QtGui.QPushButton('<', self)
        self.tape_right_button = QtGui.QPushButton('>', self)
    
        
    #
    #
    def _createTape(self):
        tptx = [QtGui.QPlainTextEdit(self) for i in xrange(GUI.TAPE_SIZE)]
        for txbx in tptx:
            txbx.setReadOnly(True)
        return tptx
        
#
#
if __name__ == '__main__':    
    main()