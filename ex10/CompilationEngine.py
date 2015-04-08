__author__ = 'Gil'


class CompilationEngine:

    def __init__(self, input, output):
        """
        creates a new compilation engine with
        the given input and output.
        """
        self.inputFile = open(input)
        self.outputFile = open(output, 'w')

        return

    def CompileClass(self):
        """
        compiles a complete class.
        """
        return

    def CompileClassVarDec(self):
        """
        compiles a static declaration or a field
        declaration.
        """
        return

    def CompileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        return

    def compileParameterList(self):
        """
        compiles a (possibly empty) parameter
        list, not including the enclosing “()”.
        """
        return

    def compileVarDec(self):
        """
        compiles a var declaration.
        """
        return

    def compileStatements(self):
        """
        compiles a sequence of statements, not
        including the enclosing “{}”.
        """
        return

    def compileDo(self):
        """
        compiles a complete class.
        """
        return

    def CompileClass(self):
        """
        Compiles a do statement
        """
        return

    def compileLet(self):
        """
        Compiles a let statement
        """
        return

    def compileWhile(self):
        """
        Compiles a while statement
        """
        return

    def compileReturn(self):
        """
        compiles a return statement.
        """
        return

    def compileIf(self):
        """
        compiles an if statement, possibly
        with a trailing else clause.
        """
        return

    def CompileExpression(self):
        """
        compiles an expression.
        """
        return

    def CompileTerm(self):
        """
        compiles a term
        """
        return

