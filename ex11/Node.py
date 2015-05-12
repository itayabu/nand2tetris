__author__ = 'ulamadm'

class Node:

    def __init__(self, parent=None):
        self.parent = parent
        self.children = {}
        self.vars = {}
        self.ifCounter = 0
        self.whileCounter = 0

    def getParent(self):
        return self.parent

    def getChild(self, name):
        return self.children[name]

    def getVar(self, name):
        return self.vars[name]

    def incIfCounter(self):
        self.ifCounter += 1
        return self.ifCounter

    def incWhileCounter(self):
        self.whileCounter += 1
        return self.whileCounter

    def addChild(self, name):
        self.children[name] = Node(self)
