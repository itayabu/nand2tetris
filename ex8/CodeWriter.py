__author__ = 'Itay'

class CodeWriter:
    def __init__(self, file):
        """
        Opens the output file/stream and gets ready to write into it.
        """
        self.file = open(file, 'w')
        self.compareCounter = 0
        self.functionCounter = 0

    def setFileName(self, fileName):
        """
        Informs the code writer that the translation of a new VM file is started.
        """
        print ("start translating file: " + fileName)

    def unaryOp(self, operation):
        commandStr = "@SP\n" + \
                     "M = M - 1\n" + \
                     "A = M\n" + \
                     "M = " + operation + "M\n" + \
                     "@SP\n" + \
                     "M = M + 1\n"
        return commandStr

    def binaryOp(self, operation):
        commandStr = "@SP\n" + \
                     "M = M - 1\n" \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@SP\n" + \
                     "M = M - 1\n" \
                     "A = M\n" + \
                     "M = M " + operation + " D\n" + \
                     "@SP\n" + \
                     "M = M + 1\n"
        return commandStr

    def compareOp(self, command):
        self.compareCounter +=1
        commandStr = "@SP\n" + \
                     "M = M - 1\n" \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@SP\n" + \
                     "M = M - 1\n" \
                     "A = M\n" + \
                     "D = M - D\n" + \
                     "@CORRECT" + str(self.compareCounter) + "\n" + \
                     "D;J"+ command.upper() + "\n" + \
                     "D = 0\n" + \
                     "@AFTER" + str(self.compareCounter) + "\n" + \
                     "0;JMP\n" + \
                     "(CORRECT" + str(self.compareCounter) + ")\n" + \
                     "D = -1\n" + \
                     "@AFTER" + str(self.compareCounter) + "\n" + \
                     "0;JMP\n" + \
                     "(AFTER" + str(self.compareCounter) + ")\n" + \
                     "@SP\n" + \
                     "A = M\n" + \
                     "M = D\n" + \
                     "@SP\n" + \
                     "M = M + 1\n"
        return commandStr


    def writeArithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given arithmetic command.
        """
        commandStr = ''
        if command == "neg":
            commandStr = self.unaryOp("-")
        elif command == "not":
            commandStr = self.unaryOp("!")
        elif command == "add":
            commandStr = self.binaryOp("+")
        elif command == "sub":
            commandStr = self.binaryOp("-")
        elif command == "and":
            commandStr = self.binaryOp("&")
        elif command == "or":
            commandStr = self.binaryOp("|")
        else:
            commandStr = self.compareOp(command)

        self.file.write(commandStr)


    segmentsCodes = {"local":"LCL", "argument":"ARG", "this":"THIS", "that":"THAT", "pointer":"3", "temp":"5"}

    def translateDict(self, segment):
        return self.segmentsCodes[segment]

    def pushToStack(self, arg):
        commandStr = "@SP\n" + \
                     "A = M\n" + \
                     "M = "+ arg + " \n" + \
                     "@SP\n" + \
                     "M = M + 1\n"
        return commandStr

    def popFromStack(self, segment, index):
        commandStr = "@" + index + "\n" + \
                     "D = A\n" + \
                     "@"+self.translateDict(segment)+"\n"
        if (segment == "local") or (segment == "that") or (segment == "this") or (segment == "argument"):
            commandStr += "A = M\n"
        commandStr += "D = A + D\n" + \
                      "@R13\n" + \
                      "M = D\n" + \
                      "@SP\n" + \
                      "M = M - 1\n" + \
                      "A = M\n" + \
                      "D = M\n" + \
                      "@R13\n" + \
                      "A = M\n" + \
                      "M = D\n"

        return commandStr

    def writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the  translation of the given command, where
        command is one of the two enumerated values: C_PUSH or C_POP
        """
        commandStr = ''
        if command == "C_PUSH":
            if segment == "temp" or segment == "pointer":
                commandStr = "@"+ index +"\n" + \
                             "D = A\n" + \
                             "@" + self.translateDict(segment) + "\n" + \
                             "A = A + D\n" + \
                             "D = M\n" + \
                             self.pushToStack("D")

            elif segment == "this" or segment == "that" or segment == "local" or segment == "argument":
                commandStr = "@"+index +"\n" + \
                             "D=A\n" + \
                             "@"+self.translateDict(segment)+"\n"+ \
                             "A = M+D\n" + \
                             "D = M\n" + \
                             self.pushToStack("D")

            elif segment == "constant": # push constant
                commandStr = "@" + index + "\n" + \
                             "D=A\n" + \
                             self.pushToStack("D")

            elif segment == "static":
                commandStr = "@"+self.file.name.split(".")[0] + "." + index + "\n" + \
                             "D = M" + \
                             self.pushToStack("D")
        else: # pop
            if segment == "static":
                commandStr = "@SP\n" + \
                             "A = M\n" + \
                             "D = M\n" + \
                             "@"+self.file.name.split(".")[0] + "." + index + "\n" + \
                             "M = D\n" + \
                             "@SP\n" + \
                             "M = M - 1\n"
            else:
                commandStr = self.popFromStack(segment, index)

        self.file.write(commandStr)

    def close(self):
        """
        Closes the output file.
        """
        self.file.close()


    def writeInit(self):
        """
        Writes the assembly code that effects the VM initialization
        """
        commandStr = "@256\n" + \
                     "D = A\n" + \
                     "@SP\n" + \
                     "M = D\n"
        commandStr += self.pushToStack("0") * 5
        self.file.write(commandStr)
        self.writeCall("Sys.init", "0")


    def writeLabel(self, label):

        """
        Writes the assembly code that is the  translation of the given label command.
        """
        self.file.write("(" + label + ")\n")

    def writeGoto(self, label):
        """
        Writes the assembly code that is the translation of the given goto command.
        """
        commandStr = "@" + label + "\n" + \
                     "0;JMP\n"
        self.file.write(commandStr)

    def writeIf(self, label):
        """
        Writes the assembly code that is the translation of the given if-goto command
        """
        commandStr = "@SP\n" + \
                     "M = M - 1\n" + \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@" + label + "\n" + \
                     "D;JNE\n"

        self.file.write(commandStr)

    def savePointers(self, pointer):
        commandStr = "@" + pointer + "\n" + \
                     "D = M\n" + \
                     self.pushToStack("D")
        return commandStr

    def writeCall(self, functionName, numArgs):
        """
        Writes the assembly code that is the translation of the given Call command.
        """
        self.functionCounter += 1
        commandStr = "@RETURN" + str(self.functionCounter) + "\n" + \
                     "D = A\n"
        # self.file.write(commandStr)
        commandStr += self.pushToStack("D")
        commandStr += self.savePointers("LCL")
        commandStr += self.savePointers("ARG")
        commandStr += self.savePointers("THIS")
        commandStr += self.savePointers("THAT")
        commandStr += "@SP\n" + \
                     "D = M\n" + \
                     "@" + str(int(numArgs) + int(5)) + "\n" + \
                     "D = D - A\n" + \
                     "@ARG\n" + \
                     "M = D\n" + \
                     "@SP\n" + \
                     "D = M\n" + \
                     "@LCL\n" + \
                     "M = D\n"
        self.file.write(commandStr)
        self.writeGoto(functionName)
        self.writeLabel("RETURN" + str(self.functionCounter))

    def restorePointers(self, pointer):
        commandStr = "@R14\n" + \
                     "M = M - 1\n" + \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@" + pointer + "\n" + \
                     "M = D\n"
        return commandStr

    def writeReturn(self):
        """
        Writes the assembly code that is the translation of the given Return command.
        """
        commandStr = "@LCL\n" + \
                     "D = M\n" + \
                     "@R14\n" + \
                     "M = D\n" + \
                     "@5\n" + \
                     "D = A\n" + \
                     "@R14\n" + \
                     "D = M - D\n" + \
                     "@R15\n" + \
                     "M = D\n"
        commandStr += self.popFromStack("argument", '0') + \
        self.restorePointers("THAT") +\
        self.restorePointers("THIS") +\
        self.restorePointers("ARG") + \
        self.restorePointers("LCL")
        commandStr += "@R15\n" + \
                      "D = M\n" + \
                      "@SP\n" + \
                      "M = D - 1\n" + \
                      "@R15\n" + \
                      "A = M\n" + \
                      "0;JMP\n"
        self.file.write(commandStr)

    def writeFunction(self, functionName, numLocals):
        """
        Writes the assembly code that is the trans. of the given Function command.
        """
        self.writeLabel(functionName)
        for i in range(int(numLocals)):
            self.file.write(self.pushToStack("0"))
