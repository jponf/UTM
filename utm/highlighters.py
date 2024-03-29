# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui
from PySide2.QtCore import Qt



class TMSourceHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.highlighting_rules = []

        # Keywords
        keyword = QtGui.QTextCharFormat()
        keyword.setForeground(QtGui.QBrush(Qt.darkMagenta, Qt.SolidPattern))
        keyword.setFontWeight(QtGui.QFont.Bold)
        keywords = ["INITIAL", "FINAL", "BLANK", "HALT"]

        for word in keywords:
            pattern = QtCore.QRegExp("^\s*\\b" + word + "\\b")
            rule = HighlightingRule(pattern, keyword)
            self.highlighting_rules.append(rule)

        # Comment
        comment = QtGui.QTextCharFormat()
        comment.setForeground(QtGui.QBrush(Qt.darkGreen, Qt.SolidPattern))
        pattern = QtCore.QRegExp("^\s*%[^\n]*")
        rule = HighlightingRule(pattern, comment)
        self.highlighting_rules.append(rule)

        # Transition symbol
        trans_sym = QtGui.QTextCharFormat()
        trans_sym.setForeground(QtGui.QBrush(Qt.red, Qt.SolidPattern))
        trans_sym.setFontWeight(QtGui.QFont.Bold)
        pattern = QtCore.QRegExp("\B->\B")
        rule = HighlightingRule(pattern, trans_sym)
        self.highlighting_rules.append(rule)

    # Overridden method
    def highlightBlock(self, text):
        for rule in self.highlighting_rules:
            expression = rule.pattern
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


class HighlightingRule:
    def __init__(self, pattern, fmt):
        self.pattern = pattern
        self.format = fmt
