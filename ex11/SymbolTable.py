__author__ = 'Gil'


class SymbolTable:

    classSymbolTable = {}

    def __init__(self):
        """Creates a new empty symbol table"""
        self.subroutineSymbolTable = {}

    def startSubroutine(self):
        """Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s scope.)"""
        self.subroutineSymbolTable.clear()

    def define(self, name, type, kind):
        """Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope. """
        self.subroutineSymbolTable[name] = (type, kind)

    def varCount(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope."""
        return len([v for (k, v) in self.subroutineSymbolTable.items() if v[1] == kind])

    def kindOf(self, name):
        """Returns the kind of the named identifier in
        the current scope. Returns NONE if the
        identifier is unknown in the current scope."""
        return

    def typeOf(self, name):
        """Returns the type of the named identifier in the current scope."""
        return

    def indexOf(self, name):
        """Returns the index assigned to named identifier."""
        return