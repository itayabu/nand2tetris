__author__ = 'Gil'


class SymbolTable:

    def __init__(self):
        """Creates a new empty symbol table"""
        self.globalScope = {}
        self.subroutinesScope = {}
        self.currScope = self.globalScope
        self.varCounter = 0
        self.argCounter = 0
        self.fieldCounter = 0
        self.staticCounter = 0
        self.ifCounter = 0
        self.whileCounter = 0

    def startSubroutine(self, name):
        """Starts a new subroutine scope (i.e. erases all names in the previous subroutine's scope.)"""
        self.subroutinesScope[name] = {}
        self.varCounter = 0
        self.argCounter = 0
        self.ifCounter = 0
        self.whileCounter = 0

    def define(self, name, type, kind):
        """Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope. """
        if kind == "static":
            self.globalScope[name] = (type, kind, self.staticCounter)
            self.staticCounter += 1
        elif kind == "field":
            self.globalScope[name] = (type, kind, self.fieldCounter)
            self.fieldCounter += 1
        elif kind == 'arg':
            self.currScope[name] = (type, kind, self.argCounter)
            self.argCounter += 1
        elif kind == 'var':
            self.currScope[name] = (type, kind, self.varCounter)
            self.varCounter += 1

    def globalsCount(self, kind):
        return len([v for (k, v) in self.globalScope.items() if v[1] == kind])

    def varCount(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope."""
        return len([v for (k, v) in self.currScope.items() if v[1] == kind])

    def typeOf(self, name):
        """Returns the type of the named identifier in the current scope."""
        if name in self.currScope:
            return self.currScope[name][0]
        if name in self.globalScope:
            return self.globalScope[name][0]
        else:
            return "NONE"

    def kindOf(self, name):
        """Returns the kind of the named identifier in
        the current scope. Returns NONE if the
        identifier is unknown in the current scope."""
        if name in self.currScope:
            return self.currScope[name][1]
        if name in self.globalScope:
            return self.globalScope[name][1]
        else:
            return "NONE"

    def indexOf(self, name):
        """Returns the index assigned to named identifier."""
        if name in self.currScope:
            return self.currScope[name][2]
        if name in self.globalScope:
            return self.globalScope[name][2]
        else:
            return "NONE"

    def setScope(self, name):
        if name == 'global':
            self.currScope = self.globalScope
        else:
            self.currScope = self.subroutinesScope[name]


