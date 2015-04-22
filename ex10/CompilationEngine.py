__author__ = 'Gil'

import JackTokenizer

class CompilationEngine:

    binaryOp = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
    unaryOp = {'-', '~'}

    def __init__(self, input, output):
        """
        creates a new compilation engine with
        the given input and output.
        """
        self.tokenizer = JackTokenizer.JackTokenizer(input)
        self.parsedRules = []
        self.outputFile = open(output, 'w')

    def writeNonTerminalStart(self, rule):
        self.outputFile.write("<"+rule+">\n")
        self.parsedRules.append(rule)

    def writeNonTerminalEnd(self):
        rule = self.parsedRules.pop()
        self.outputFile.write("</"+rule+">\n")

    def writeTerminal(self, token, value):
        self.outputFile.write("<"+token+"> "+value+" </"+token+">\n")

    def advance(self):
        token, value = self.tokenizer.advance()
        self.writeTerminal(token, value)

    def nextTokenValueIs(self, val):
        token, value = self.tokenizer.peek()
        return value is val

    def compileClass(self):
        """
        compiles a complete class.
        """
        self.writeNonTerminalStart('class')
        self.advance() #get 'class' keyword
        self.advance() #get class name
        self.advance() #get '{' symbol
        if self.existClassVarDec():
            self.compileClassVarDec()
        while self.existSubroutine():
            self.compileSubroutine()
        self.writeNonTerminalEnd()

    def existClassVarDec(self):
        return self.nextTokenValueIs("static") or self.nextTokenValueIs("field")

    def existSubroutine(self):
        return self.nextTokenValueIs("constructor") or self.nextTokenValueIs("method")\
               or self.nextTokenValueIs("function")

    def compileClassVarDec(self):
        """
        compiles a static declaration or a field
        declaration.
        """
        self.writeNonTerminalStart('classVarDec')
        while self.existClassVarDec():
            self.writeClassVarDec()
        self.writeNonTerminalEnd()

    def writeClassVarDec(self):
        self.advance() #get 'static' or 'field'
        self.advance() #get var type
        self.advance() #get var name
        self.advance() #get ';' symbol

    def compileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        self.writeNonTerminalStart('subroutineDec')
        self.advance() #get subroutine type
        self.advance() #get subroutine return type / 'constructor'
        self.advance() #get subroutine name / 'new'
        self.advance() #get '(' symbol
        self.compileParameterList()
        self.advance() #get ')' symbol
        self.compileSubroutineBody()
        self.writeNonTerminalEnd()


    def compileParameterList(self):
        """
        compiles a (possibly empty) parameter
        list, not including the enclosing “()”.
        """
        self.writeNonTerminalStart('parameterList')
        while self.existParameter():
            self.writeParam()
        self.writeNonTerminalEnd()

    def existParameter(self):
        token, value = self.tokenizer.peek()
        return not (token is "symbol")

    def writeParam(self):
        self.advance() #get parameter type
        self.advance() #get parameter name
        if self.existAnotherParam():
            self.advance() #get ',' symbol

    def existAnotherParam(self):
        return self.nextTokenValueIs(",")

    def compileSubroutineBody(self):
        self.writeNonTerminalStart('subroutineBody')
        self.advance() #get '{' symbol
        while self.existVarDec():
            self.compileVarDec()
        self.compileStatements()
        self.advance() #get '}' symbol
        self.writeNonTerminalEnd()

    def existVarDec(self):
        return self.nextTokenValueIs("var")

    def compileVarDec(self):
        """
        compiles a var declaration.
        """
        self.writeNonTerminalStart('varDec')
        self.advance() #get 'var' keyword
        self.advance() #get var type
        self.advance() #get var name
        self.advance() #get ';' symbol
        self.writeNonTerminalEnd()

    def compileStatements(self):
        """
        compiles a sequence of statements, not
        including the enclosing “{}”.
        """
        self.writeNonTerminalStart('statements')
        while self.existStatement():
            if   self.nextTokenValueIs("do"):     self.compileDo()
            elif self.nextTokenValueIs("let"):    self.compileLet()
            elif self.nextTokenValueIs("if"):     self.compileIf()
            elif self.nextTokenValueIs("while"):  self.compileWhile()
            elif self.nextTokenValueIs("return"): self.compileReturn()
        self.writeNonTerminalEnd()

    def existStatement(self):
        return self.nextTokenValueIs("do") \
            or self.nextTokenValueIs("let")\
            or self.nextTokenValueIs("if")\
            or self.nextTokenValueIs("while")\
            or self.nextTokenValueIs("return")\

    def compileDo(self):
        """
        compiles a do statement
        """
        self.writeNonTerminalStart('doStatement')
        self.advance() #get 'do' keyword
        self.compileSubroutineCall()
        self.advance() #get ';' symbol
        self.writeNonTerminalEnd()

    def compileSubroutineCall(self):
        self.advance() #get class/subroutine/var name
        if self.objectSubroutineCall():
            self.advance() #get '.' symbol
            self.advance() #get subroutine name
        self.advance() #get '(' symbol
        self.compileExpressionList()

    def objectSubroutineCall(self):
        return self.nextTokenValueIs(".")

    def compileExpressionList(self):
        if self.existExpression():
            self.compileExpression()
        while self.existAnotherExpression():
            self.advance() #get ',' symbol
            self.compileExpression()
        self.advance() #get ')' symbol

    def existAnotherExpression(self):
        return self.nextTokenValueIs(",")

    def compileLet(self):
        """
        compiles a let statement
        """
        self.writeNonTerminalStart('letStatement')
        self.advance() #get 'let' keyword
        self.advance() #get var name
        if self.existArrayIndex():
            self.writeArrayIndex()
        self.advance() #get '='
        self.compileExpression()
        self.advance() #get ';' symbol
        self.writeNonTerminalEnd()

    def existArrayIndex(self):
        self.nextTokenValueIs("[")

    def writeArrayIndex(self):
        self.advance() #get '[' symbol
        self.compileExpression()
        self.advance() #get ']' symbol

    def compileWhile(self):
        """
        compiles a while statement
        """
        self.writeNonTerminalStart('whileStatement')
        self.advance() #get 'while' keyword
        self.advance() #get '(' symbol
        self.compileExpression()
        self.advance() #get ')' symbol
        self.advance() #get '{' symbol
        self.compileStatements()
        self.advance() #get '}' symbol
        self.writeNonTerminalEnd()

    def compileReturn(self):
        """
        compiles a return statement.
        """
        self.writeNonTerminalStart('returnStatement')
        self.advance() #get 'return' keyword
        while self.existExpression():
            self.compileExpression()
        self.writeNonTerminalEnd()

    def existExpression(self):
        return self.existTerm()

    def existTerm(self):
        #TODO: complete
        return

    def compileIf(self):
        """
        compiles an if statement, possibly
        with a trailing else clause.
        """
        self.writeNonTerminalStart('ifStatement')
        self.advance() #get 'if' keyword
        self.advance() #get '(' symbol
        self.compileExpression()
        self.advance() #get ')' symbol
        self.advance() #get '{' symbol
        self.compileStatements()
        self.advance() #get '}' symbol
        if self.existElse():
            self.advance() #get 'else' keyword
            self.advance() #get '{' symbol
            self.compileStatements()
            self.advance() #get '}' symbol
        self.writeNonTerminalEnd()

    def existElse(self):
        self.nextTokenValueIs("else")

    def compileExpression(self):
        """
        compiles an expression.
        """
        self.writeNonTerminalStart('expression')
        self.compileTerm()
        while self.existBinaryOp():
            self.advance() #get op symbol
            self.compileTerm()
        self.writeNonTerminalEnd()

    def existUnaryOp(self):
        token, value = self.tokenizer.peek()
        return (value in self.unaryOp)

    def existBinaryOp(self):
        token, value = self.tokenizer.peek()
        return (value in self.binaryOp)

    def compileTerm(self):
        """
        compiles a term
        """
        self.writeNonTerminalStart('term')
        if self.existUnaryOp():
            self.advance() #get unary operation symbol
            self.compileTerm()
        elif self.nextTokenValueIs("("):
            self.advance() #get '(' symbol
            self.compileExpression()
            self.advance() #get ')' symbol
        #TODO: complete
        self.writeNonTerminalEnd()
