__author__ = 'Gil'

import JackTokenizer
import SymbolTable
import VMWriter


class CompilationEngine:

    binaryOp = {'+', '-', '*', '/', '|', '=', '<', '>', '&'}
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
        self.name = ''

    def advance(self):
        return self.tokenizer.advance()

    def nextValueIn(self, list):
        token, value = self.tokenizer.peek()
        return value in list

    def nextValueIs(self, val):
        token, value = self.tokenizer.peek()
        return value == val

    def nextTokenIs(self, tok):
        token, value = self.tokenizer.peek()
        return token == tok

    def doublePeak(self, tok):
        token, value = self.tokenizer.doublePeek()
        self.writer.writeArithmetic(token)
        self.writer.writeArithmetic(value)
        return token == tok

    def compileClass(self):
        """
        compiles a complete class.
        """
        self.advance()  # get 'class' keyword
        self.className = self.advance()[1]  # get class name
        self.advance()  # get '{' symbol
        if self.existClassVarDec():
            self.compileClassVarDec()
        while self.existSubroutine():
            self.compileSubroutine()
        self.advance()  # get '}' symbol
        self.writer.close()

    def existClassVarDec(self):
        return self.nextValueIs("static") or self.nextValueIs("field")

    def existSubroutine(self):
        return self.nextValueIs("constructor") or self.nextValueIs("method") \
               or self.nextValueIs("function")

    def compileClassVarDec(self):
        """
        compiles a static declaration or a field
        declaration.
        """
        while self.existClassVarDec():
            self.writeClassVarDec()

    def writeClassVarDec(self):
        kind = self.advance()[1]  # get 'static' or 'field'
        type = self.advance()[1]  # get var type
        name = self.advance()[1]  # get var name
        self.symbolTable.define(name, type, kind)
        while self.nextValueIs(","):
            self.advance()  # get ',' symbol
            name = self.advance()[1]  # get var name
            self.symbolTable.define(name, type, kind)
        self.advance()  # get ';' symbol

    def compileSubroutine(self):
        """
        compiles a complete method, function,
        or constructor.
        """
        funcType = self.advance()  # get subroutine type / 'constructor'
        self.advance()  # get subroutine return type / class name
        self.name = self.className + '.' + self.advance()[1]  # get subroutine name / 'new'
        self.symbolTable.startSubroutine(self.name)
        self.symbolTable.setScope(self.name)
        self.advance()  # get '(' symbol
        self.compileParameterList(funcType)
        self.advance()  # get ')' symbol
        self.compileSubroutineBody(funcType)


    def compileParameterList(self,funcType):
        """
        compiles a (possibly empty) parameter
        list, not including the enclosing "()".
        """
        if funcType[1] == "method":
            self.symbolTable.define("this", "self", 'arg')
        while self.existParameter():
            self.writeParam()

    def existParameter(self):
        return not self.nextTokenIs("symbol")

    def writeParam(self):
        type = self.advance()[1]  # get parameter type
        name = self.advance()[1]  # get parameter name
        self.symbolTable.define(name, type, 'arg')
        if self.nextValueIs(","):
            self.advance()  # get ',' symbol


    def compileSubroutineBody(self, funcType):
        self.advance()  # get '{' symbol
        while self.existVarDec():
            self.compileVarDec()
        nVars = self.symbolTable.varCount('var')
        self.writer.writeFunction(self.name, nVars)
        self.loadPointer(funcType)
        self.compileStatements()
        self.advance()  # get '}' symbol
        self.symbolTable.setScope('global')

    def loadPointer(self, funcType):
        if funcType[1] == "method":
            self.writer.writePush('argument', 0)
            self.writer.writePop('pointer', 0)
        if funcType[1] == 'constructor':
            globalVars = self.symbolTable.globalsCount('field')
            self.writer.writePush('constant', globalVars)
            self.writer.writeCall('Memory.alloc', 1)
            self.writer.writePop('pointer', 0)

    def existVarDec(self):
        return self.nextValueIs("var")

    def compileVarDec(self):
        """
        compiles a var declaration.
        """
        kind = self.advance()[1]  # get 'var' keyword
        type = self.advance()[1]  # get var type
        name = self.advance()[1]  # get var name
        self.symbolTable.define(name, type, kind)
        while self.nextValueIs(","):
            self.advance()  # get ',' symbol
            name = self.advance()[1]  # get next var name
            self.symbolTable.define(name, type, kind)
        self.advance()  # get ';' symbol

    def compileStatements(self):
        """
        compiles a sequence of statements, not
        including the enclosing "{}".
        """
        while self.existStatement():
            if   self.nextValueIs("do"):     self.compileDo()
            elif self.nextValueIs("let"):    self.compileLet()
            elif self.nextValueIs("if"):     self.compileIf()
            elif self.nextValueIs("while"):  self.compileWhile()
            elif self.nextValueIs("return"): self.compileReturn()

    def existStatement(self):
        return (self.nextValueIs("do") \
                or self.nextValueIs("let") \
                or self.nextValueIs("if") \
                or self.nextValueIs("while") \
                or self.nextValueIs("return"))

    def compileDo(self):
        """
        compiles a do statement
        """
        self.advance()  # get 'do' keyword
        self.compileSubroutineCall()
        self.writer.writePop('temp', 0)
        self.advance()  # get ';' symbol

    def compileSubroutineCall(self):
        firstName = lastName = fullName = ''
        nLocals = 0
        firstName = self.advance()[1]  # get class/subroutine/var name
        if self.nextValueIs("."):  # case of className.subroutineName
            self.advance()  # get '.' symbol
            lastName = self.advance()[1]  # get subroutine name
            if firstName in self.symbolTable.currScope or firstName in self.symbolTable.globalScope:
                self.writePush(firstName, lastName)
                fullName = self.symbolTable.typeOf(firstName) + '.' + lastName
                nLocals += 1
            else:
                fullName = firstName + '.' + lastName
        else:
            self.writer.writePush('pointer', 0)
            nLocals += 1
            fullName = self.className + '.' + firstName
        self.advance()  # get '(' symbol
        nLocals += self.compileExpressionList()
        self.writer.writeCall(fullName, nLocals)
        self.advance()  # get ')' symbol

    def compileExpressionList(self):
        counter = 0
        if self.existExpression():
            self.compileExpression()
            counter += 1
        while self.nextValueIs(","):  # case of multiple expressions
            self.advance()  # get ',' symbol
            self.compileExpression()
            counter += 1
        return counter

    def compileLet(self):
        """
        compiles a let statement
        """
        self.advance()  # get 'let' keyword
        isArray = False
        name = self.advance()[1]  # get var name
        if self.nextValueIs("["):  # case of varName[expression]
            isArray = True
            self.compileArrayIndex(name)
        self.advance()  # get '='
        self.compileExpression()
        if isArray:
            self.writer.writePop("temp", 0)
            self.writer.writePop("pointer", 1)
            self.writer.writePush("temp", 0)
            self.writer.writePop("that", 0)
        else:
            self.writePop(name)
        self.advance()  # get ';' symbol

    def compileArrayIndex(self, name):
        self.writeArrayIndex()
        if name in self.symbolTable.currScope:
            if self.symbolTable.kindOf(name) == 'var':
                self.writer.writePush('local', self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == 'arg':
                self.writer.writePush('argument', self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == 'static':
                self.writer.writePush('static', self.symbolTable.indexOf(name))
            else:
                self.writer.writePush('this', self.symbolTable.indexOf(name))
        self.writer.writeArithmetic('add')


    def writeArrayIndex(self):
        self.advance()  # get '[' symbol
        self.compileExpression()
        self.advance()  # get ']' symbol

    def compileWhile(self):
        """
        compiles a while statement
        """
        whileCounter = str(self.symbolTable.whileCounter)
        self.symbolTable.whileCounter += 1
        self.writer.writeLabel('WHILE_EXP' + whileCounter)
        self.advance()  # get 'while' keyword
        self.advance()  # get '(' symbol
        self.compileExpression()
        self.writer.writeArithmetic('not')
        self.writer.writeIf('WHILE_END' + whileCounter)
        self.advance()  # get ')' symbol
        self.advance()  # get '{' symbol
        self.compileStatements()
        self.writer.writeGoto('WHILE_EXP' + whileCounter)
        self.writer.writeLabel('WHILE_END' + whileCounter)
        self.advance()  # get '}' symbol

    def compileReturn(self):
        """
        compiles a return statement.
        """
        self.advance()  # get 'return' keyword
        returnEmpty = True
        while self.existExpression():
            returnEmpty = False
            self.compileExpression()
        if (returnEmpty):
            self.writer.writePush('constant', 0)
        self.writer.writeReturn()
        self.advance()  # get ';' symbol

    def existExpression(self):
        return self.existTerm()

    def existTerm(self):
        token, value = self.tokenizer.peek()
        return self.nextTokenIs("integerConstant") or self.nextTokenIs("stringConstant") \
               or self.nextTokenIs("identifier") or (self.nextValueIn(self.unaryOp)) \
               or (self.nextValueIn(self.keywordConstant)) or (self.nextValueIs('('))

    def compileIf(self):
        """
        compiles an if statement, possibly
        with a trailing else clause.
        """
        self.advance()  # get 'if' keyword
        self.advance()  # get '(' symbol
        self.compileExpression()
        self.advance()  # get ')' symbol
        currentCounter = self.symbolTable.ifCounter
        self.symbolTable.ifCounter += 1
        self.writer.writeIf('IF_TRUE' + str(currentCounter))
        self.writer.writeGoto('IF_FALSE' + str(currentCounter))
        self.writer.writeLabel('IF_TRUE' + str(currentCounter))
        self.advance()  # get '{' symbol
        self.compileStatements()
        self.advance()  # get '}' symbol
        if self.nextValueIs("else"):
            self.writer.writeGoto('IF_END' + str(currentCounter))
            self.writer.writeLabel('IF_FALSE' + str(currentCounter))
            self.advance()  # get 'else' keyword
            self.advance()  # get '{' symbol
            self.compileStatements()
            self.advance()  # get '}' symbol
            self.writer.writeLabel('IF_END' + str(currentCounter))
        else:
            self.writer.writeLabel('IF_FALSE' + str(currentCounter))

    def compileExpression(self):
        """
        compiles an expression.
        """
        self.compileTerm()
        while self.nextValueIn(self.binaryOp):
            op = self.advance()[1]  # get op symbol
            self.compileTerm()
            if op == '+':
                self.writer.writeArithmetic('add')
            elif op == '-':
                self.writer.writeArithmetic('sub')
            elif op == '*':
                self.writer.writeCall('Math.multiply', 2)
            elif op == '/':
                self.writer.writeCall('Math.divide', 2)
            elif op == '|':
                self.writer.writeArithmetic('or')
            elif op == '&':
                self.writer.writeArithmetic('and')
            elif op == '=':
                self.writer.writeArithmetic('eq')
            elif op == '<':
                self.writer.writeArithmetic('lt')
            elif op == '>':
                self.writer.writeArithmetic('gt')

    def compileTerm(self):
        """
        compiles a term
        """
        array = False
        if self.nextTokenIs("integerConstant"):
            value = self.advance()[1]  # get constant
            self.writer.writePush('constant', value)
        elif self.nextTokenIs("stringConstant"):
            value = self.advance()[1]  # get string
            self.writer.writePush('constant', len(value))
            self.writer.writeCall('String.new', 1)
            for letter in value:
                self.writer.writePush('constant', ord(letter))
                self.writer.writeCall('String.appendChar', 2)
        elif self.nextValueIn(self.keywordConstant):
            value = self.advance()[1]  # get keywordConstant
            if value == "this":
                self.writer.writePush('pointer', 0)
            else:
                self.writer.writePush('constant', 0)
                if value == "true":
                    self.writer.writeArithmetic('not')
        elif self.nextTokenIs("identifier"):
            nLocals = 0
            name = self.advance()[1]  # get class/var/func name
            if self.nextValueIs("["):  # case of varName[expression]
                array = True
                self.compileArrayIndex(name)
            if self.nextValueIs("("):
                nLocals += 1
                self.writer.writePush('pointer', 0)
                self.advance()  # get '(' symbol
                nLocals += self.compileExpressionList()
                self.advance()  # get ')' symbol
                self.writer.writeCall(self.className + '.' + name, nLocals)
            elif self.nextValueIs("."):  # case of subroutine call
                self.advance()  # get '.' symbol
                lastName = self.advance()[1]  # get subroutine name
                if name in self.symbolTable.currScope or name in self.symbolTable.globalScope:
                    self.writePush(name, lastName)
                    name = self.symbolTable.typeOf(name) + '.' + lastName
                    nLocals += 1
                else:
                    name = name + '.' + lastName
                self.advance()  # get '(' symbol
                nLocals += self.compileExpressionList()
                self.advance()  # get ')' symbol
                self.writer.writeCall(name, nLocals)
            else:
                if array:
                    self.writer.writePop('pointer', 1)
                    self.writer.writePush('that', 0)
                elif name in self.symbolTable.currScope:
                    if self.symbolTable.kindOf(name) == 'var':
                        self.writer.writePush('local', self.symbolTable.indexOf(name))
                    elif self.symbolTable.kindOf(name) == 'arg':
                        self.writer.writePush('argument', self.symbolTable.indexOf(name))
                else:
                    if self.symbolTable.kindOf(name) == 'static':
                        self.writer.writePush('static', self.symbolTable.indexOf(name))
                    else:
                        self.writer.writePush('this', self.symbolTable.indexOf(name))
        elif self.nextValueIn(self.unaryOp):
            op = self.advance()[1]  # get unary operation symbol
            self.compileTerm()
            if op == '-':
                self.writer.writeArithmetic('neg')
            elif op == '~':
                self.writer.writeArithmetic('not')
        elif self.nextValueIs("("):
            self.advance()  # get '(' symbol
            self.compileExpression()
            self.advance()  # get ')' symbol

    def writePush(self, name, lastName):
        if name in self.symbolTable.currScope:
            if self.symbolTable.kindOf(name) == 'var':
                self.writer.writePush('local', self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == 'arg':
                self.writer.writePush('argument', self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == 'static':
                self.writer.writePush('static', self.symbolTable.indexOf(name))
            else:
                self.writer.writePush('this', self.symbolTable.indexOf(name))

    def writePop(self, name):
        if name in self.symbolTable.currScope:
            if self.symbolTable.kindOf(name) == 'var':
                self.writer.writePop('local', self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == 'arg':
                self.writer.writePop('argument', self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == 'static':
                self.writer.writePop('static', self.symbolTable.indexOf(name))
            else:
                self.writer.writePop('this', self.symbolTable.indexOf(name))