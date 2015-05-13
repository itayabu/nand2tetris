__author__ = 'Gil'

import Node

class SymbolTable:

    def __init__(self):
        """Creates a new empty symbol table"""
        self.globalScope = {}
        self.subroutinesScope = {}
        self.currScope = self.globalScope

    def startSubroutine(self, name):
        """Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)"""
        self.subroutinesScope[name] = {}

    def define(self, name, type, kind):
        """Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope. """
        if kind == "STATIC" or kind == "FIELD":
            self.globalScope[name] = (type, kind, len(self.globalScope))
        else:
            self.currScope[name] = (type, kind, len(self.currScope))

    def globalsCount(self, kind):
        return len([v for (k, v) in self.globalScope.items() if v[1] == kind])

    def varCount(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope."""
        return len([v for (k, v) in self.currScope.items() if v[1] == kind])

    def typeOf(self, name):
        """Returns the type of the named identifier in the current scope."""
        return self.currScope[name][0] if (name in self.currScope) else "NONE"

    def kindOf(self, name):
        """Returns the kind of the named identifier in
        the current scope. Returns NONE if the
        identifier is unknown in the current scope."""
        return self.currScope[name][1] if (name in self.currScope) else "NONE"

    def indexOf(self, name):
        """Returns the index assigned to named identifier."""
        return self.currScope[name][2] if (name in self.currScope) else "NONE"

    def setScope(self, name):
        if name == 'global':
            self.currScope = self.globalScope
        else:
            self.currScope = self.subroutinesScope[name]


