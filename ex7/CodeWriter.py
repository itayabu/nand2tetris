__author__ = 'Itay'

class CodeWriter:
    def __init__(self, file):
        """
        Opens the output file/stream and gets ready to write into it.
        """
        self.file = open(file, 'w')
        self.counter = 0

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
        self.counter +=1
        commandStr = "@SP\n" + \
                     "M = M - 1\n" \
                     "A = M\n" + \
                     "D = M\n" + \
                     "@SP\n" + \
                     "M = M - 1\n" \
                     "A = M\n" + \
                     "D = M - D\n" + \
                     "@CORRECT" + str(self.counter) + "\n" + \
                     "D;J"+ command.upper() + "\n" + \
                     "D = 0\n" + \
                     "@AFTER" + str(self.counter) + "\n" + \
                     "0;JMP\n" + \
                     "(CORRECT" + str(self.counter) + ")\n" + \
                     "D = -1\n" + \
                     "@AFTER" + str(self.counter) + "\n" + \
                     "0;JMP\n" + \
                     "(AFTER" + str(self.counter) + ")\n" + \
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

    def push2stack(self):
        commandStr = "@SP\n" + \
                     "A = M\n" + \
                     "M = D\n" + \
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
                             self.push2stack()

            elif segment == "this" or segment == "that" or segment == "local" or segment == "argument":
                commandStr = "@"+index +"\n" + \
                             "D=A\n" + \
                             "@"+self.translateDict(segment)+"\n"+ \
                             "A = M+D\n" + \
                             "D = M\n" + \
                             self.push2stack()

            elif segment == "constant": # push constant
                commandStr = "@" + index + "\n" + \
                             "D=A\n" + \
                             self.push2stack()

            elif segment == "static":
                commandStr = "@"+self.file.name.split(".")[0] + "." + index + "\n" + \
                             "D = M" + \
                             self.push2stack()
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