__author__ = 'Gil'

import JackTokenizer
import SymbolTable
import VMWriter


class CompilationEngine:

    binaryOp = {'+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;'}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}

    def __init__(self, input, output):
        """
        creates a new compilation engine with
        the given input and output.
        """
        self.tokenizer = JackTokenizer.JackTokenizer(input)
        self.writer = VMWriter.VMWriter(output)
        self.symbolTable = SymbolTable.SymbolTable()
        self.className = ''
        #self.parsedRules = []
        #self.outputFile = open(output, 'w')
        #self.indent = ""

    # def addIndent(self):
    #     self.indent += "  "
    #
    # def deleteIndent(self):
    #     self.indent = self.indent[:-2]

    # def writeNonTerminalStart(self, rule):
    #     self.outputFile.write(self.indent+"<"+rule+">\n")
    #     self.parsedRules.append(rule)
    #     self.addIndent()
    #
    # def writeNonTerminalEnd(self):
    #     self.deleteIndent()
    #     rule = self.parsedRules.pop()
    #     self.outputFile.write(self.indent+"</"+rule+">\n")
    #
    # def writeTerminal(self, token, value):
    #     self.outputFile.write(self.indent+"<"+token+"> "+value+" </"+token+">\n")

    def advance(self):
        return self.tokenizer.advance()
        #self.writeTerminal(token, value)

    def nextValueIn(self, list):
        token, value = self.tokenizer.peek()
        return value in list

    def nextValueIs(self, val):
        token, value = self.tokenizer.peek()
        return value == val

    def nextTokenIs(self, tok):
        token, value = self.tokenizer.peek()
        return token == tok

    def compileClass(self):
        """
        compiles a complete class.
        """
        # self.writeNonTerminalStart('class')
        self.advance()  # get 'class' keyword
        self.className = self.advance()[2]  # get class name
        self.advance()  # get '{' symbol
        if self.existClassVarDec():
            self.compileClassVarDec()
        while self.existSubroutine():
            self.compileSubroutine()
        self.advance() #get '}' symbol
        # self.writeNonTerminalEnd()
        # self.outputFile.close()
        self.writer.close()

    def existClassVarDec(self):
        return self.nextValueIs("static") or self.nextValueIs("field")

    def existSubroutine(self):
        return self.nextValueIs("constructor") or self.nextValueIs("method")\
               or self.nextValueIs("function")

    def compileClassVarDec(self):
        """
        compiles a static declaration or a field
        declaration.
        """
        while self.existClassVarDec():
            #self.writeNonTerminalStart('classVarDec')
            self.writeClassVarDec()
            #self.writeNonTerminalEnd()

    def writeClassVarDec(self):
        kind = self.advance()[2]  # get 'static' or 'field'
        type = self.advance()[2]  # get var type
        name = self.advance()[2]  # get var name
        self.symbolTable.define(name, type, kind)
        while self.nextValueIs(","):
            self.advance()  # get ',' symbol
            name = self.advance()  # get var name
            self.symbolTable.define(name, type, kind)
        self.advance()  # get ';' symbol

    def compileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        #self.writeNonTerminalStart('subroutineDec')
        self.advance()  # get subroutine type / 'constructor'
        self.advance()  # get subroutine return type / class name
        name = self.className + '.' + self.advance()  # get subroutine name / 'new'
        self.advance()  # get '(' symbol
        nArgs = self.compileParameterList()
        self.writer.writeFunction(name, nArgs)
        self.advance()  # get ')' symbol
        self.compileSubroutineBody()
        #self.writeNonTerminalEnd()


    def compileParameterList(self):
        """
        compiles a (possibly empty) parameter
        list, not including the enclosing “()”.
        """
        #self.writeNonTerminalStart('parameterList')
        counter = 0
        while self.existParameter():
            self.writeParam()
            counter += 1
        return counter
        #self.writeNonTerminalEnd()

    def existParameter(self):
        return not self.nextTokenIs("symbol")

    def writeParam(self):
        self.advance()  # get parameter type
        self.advance()  # get parameter name
        if self.nextValueIs(","):
            self.advance()  # get ',' symbol


    def compileSubroutineBody(self):
        #self.writeNonTerminalStart('subroutineBody')
        self.advance()  # get '{' symbol
        while self.existVarDec():
            self.compileVarDec()
        self.compileStatements()
        self.advance()  # get '}' symbol
        #self.writeNonTerminalEnd()

    def existVarDec(self):
        return self.nextValueIs("var")

    def compileVarDec(self):
        """
        compiles a var declaration.
        """
        #self.writeNonTerminalStart('varDec')
        self.advance()  # get 'var' keyword
        self.advance()  # get var type
        self.advance()  # get var name
        self.advance()  # get ';' symbol
        #self.writeNonTerminalEnd()

    def compileStatements(self):
        """
        compiles a sequence of statements, not
        including the enclosing “{}”.
        """
        #self.writeNonTerminalStart('statements')
        while self.existStatement():
            if   self.nextValueIs("do"):     self.compileDo()
            elif self.nextValueIs("let"):    self.compileLet()
            elif self.nextValueIs("if"):     self.compileIf()
            elif self.nextValueIs("while"):  self.compileWhile()
            elif self.nextValueIs("return"): self.compileReturn()
        #self.writeNonTerminalEnd()

    def existStatement(self):
        return self.nextValueIs("do") \
            or self.nextValueIs("let")\
            or self.nextValueIs("if")\
            or self.nextValueIs("while")\
            or self.nextValueIs("return")\

    def compileDo(self):
        """
        compiles a do statement
        """
        #self.writeNonTerminalStart('doStatement')
        self.advance()  # get 'do' keyword
        self.compileSubroutineCall()
        self.advance()  # get ';' symbol
        #self.writeNonTerminalEnd()

    def compileSubroutineCall(self):
        self.advance()  # get class/subroutine/var name
        if self.nextValueIs("."):  # case of className.subroutineName
            self.advance()  # get '.' symbol
            self.advance()  # get subroutine name
        self.advance()  # get '(' symbol
        self.compileExpressionList()
        self.advance()  # get ')' symbol

    def compileExpressionList(self):
        #self.writeNonTerminalStart('expressionList')
        if self.existExpression():
            self.compileExpression()
        while self.nextValueIs(","):  # case of multiple expressions
            self.advance()  # get ',' symbol
            self.compileExpression()
        #self.writeNonTerminalEnd()

    def compileLet(self):
        """
        compiles a let statement
        """
        #self.writeNonTerminalStart('letStatement')
        self.advance()  # get 'let' keyword
        self.advance()  # get var name
        if self.nextValueIs("["): #case of varName[expression]
            self.writeArrayIndex()
        self.advance()  # get '='
        self.compileExpression()
        self.advance()  # get ';' symbol
        #self.writeNonTerminalEnd()

    def writeArrayIndex(self):
        self.advance()  # get '[' symbol
        self.compileExpression()
        self.advance()  # get ']' symbol

    def compileWhile(self):
        """
        compiles a while statement
        """
        #self.writeNonTerminalStart('whileStatement')
        self.advance()  # get 'while' keyword
        self.advance()  # get '(' symbol
        self.compileExpression()
        self.advance()  # get ')' symbol
        self.advance()  # get '{' symbol
        self.compileStatements()
        self.advance()  # get '}' symbol
        #self.writeNonTerminalEnd()

    def compileReturn(self):
        """
        compiles a return statement.
        """
        #self.writeNonTerminalStart('returnStatement')
        self.advance()  # get 'return' keyword
        while self.existExpression():
            self.compileExpression()
        self.advance()  # get ';' symbol
        #self.writeNonTerminalEnd()

    def existExpression(self):
        return self.existTerm()

    def existTerm(self):
        token, value = self.tokenizer.peek()
        return self.nextTokenIs("integerConstant") or self.nextTokenIs("stringConstant")\
               or self.nextTokenIs("identifier") or (self.nextValueIn(self.unaryOp))\
               or (self.nextValueIn(self.keywordConstant)) or (self.nextValueIs('('))

    def compileIf(self):
        """
        compiles an if statement, possibly
        with a trailing else clause.
        """
        #self.writeNonTerminalStart('ifStatement')
        self.advance()  # get 'if' keyword
        self.advance()  # get '(' symbol
        self.compileExpression()
        self.advance()  # get ')' symbol
        self.advance()  # get '{' symbol
        self.compileStatements()
        self.advance()  # get '}' symbol
        if self.nextTokenIs("else"):
            self.advance()  # get 'else' keyword
            self.advance()  # get '{' symbol
            self.compileStatements()
            self.advance()  # get '}' symbol
        #self.writeNonTerminalEnd()

    def compileExpression(self):
        """
        compiles an expression.
        """
        #self.writeNonTerminalStart('expression')
        self.compileTerm()
        while self.nextValueIn(self.binaryOp):
            self.advance()  # get op symbol
            self.compileTerm()
        #self.writeNonTerminalEnd()

    def compileTerm(self):
        """
        compiles a term
        """
        #self.writeNonTerminalStart('term')
        if self.nextTokenIs("integerConstant") or self.nextTokenIs("stringConstant")\
                or (self.nextValueIn(self.keywordConstant)):
            self.advance()  # get constant
        elif self.nextTokenIs("identifier"):
            self.advance()  # get class/var name
            if self.nextValueIs("["):  # case of varName[expression]
                self.writeArrayIndex()
            if self.nextValueIs("."):  # case of subroutine call
                self.advance()  # get '.' symbol
                self.advance()  # get subroutine name
                self.advance()  # get '(' symbol
                self.compileExpressionList()
                self.advance()  # get ')' symbol
        elif self.nextValueIn(self.unaryOp):
            self.advance()  # get unary operation symbol
            self.compileTerm()
        elif self.nextValueIs("("):
            self.advance()  # get '(' symbol
            self.compileExpression()
            self.advance()  # get ')' symbol
        #self.writeNonTerminalEnd()
