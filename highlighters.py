# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

class TMSourceHightlighter(QtGui.QSyntaxHighlighter):
    
    #
    #
    def __init__(self, parent, theme):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        #super(TMSourceHightlighter, self).__init__(self, parent)
        
        self.parent = parent        
        self.highlighting_rules = []
        
        # Formats
        keyword = QtGui.QTextCharFormat()
        
        # HALT
        brush = QtGui.QBrush( Qt.darkBlue, Qt.SolidPattern )
        keyword.setForeground( brush )
        keyword.setFontWeight( QtGui.QFont.Bold )
        keywords = QtCore.QStringList( ["INITIAL", "FINAL", "BLANK", "HALT"])
        
        for word in keywords:
            pattern = QtCore.QRegExp("^\s*\\b" + word + "\\b")
            rule = HighlightingRule(pattern, keyword)
            self.highlighting_rules.append( rule )
            
    #
    #   Overrided method
    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            expression = rule.pattern
            index = expression.indexIn( text )
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat( index, length, rule.format )
                index = text.indexOf( expression, index + length )
                
        self.setCurrentBlockState( 0 )
        
class HighlightingRule:
    
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format