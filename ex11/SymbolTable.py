__author__ = 'Gil'

import Node

class SymbolTable:

    def __init__(self):
        """Creates a new empty symbol table"""
        self.NodeTable = Node.Node()
        self.currScope = self.NodeTable

    # def startSubroutine(self):
    #     """Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)"""
    #     self.subroutineSymbolTable.clear()

    def define(self, name, type, kind):
        """Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope. """
        if kind == "STATIC" or kind == "FIELD":
            self.NodeTable.vars[name] = (type, kind, len(self.NodeTable.vars))
        else:
            self.currScope.vars[name] = (type, kind, len(self.currScope.vars))

    def globalsCount(self, kind):
        return len([v for (k, v) in self.NodeTable.vars.items() if v[1] == kind])

    def varCount(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope."""
        return len([v for (k, v) in self.currScope.vars.items() if v[1] == kind])

    def kindOf(self, name):
        """Returns the kind of the named identifier in
        the current scope. Returns NONE if the
        identifier is unknown in the current scope."""
        return self.currScope.vars[name][1] if (name in self.currScope.vars) else "NONE"

    def typeOf(self, name):
        """Returns the type of the named identifier in the current scope."""
        return self.currScope.vars[name][0] if (name in self.currScope.vars) else "NONE"

    def indexOf(self, name):
        """Returns the index assigned to named identifier."""
        return self.currScope.vars[name][2] if (name in self.currScope.vars) else "NONE"

    def setScope(self, name):
        if name == 'parent':
            self.currScope = self.currScope.getParent()
        else:
            self.currScope = self.currScope.children[name]
