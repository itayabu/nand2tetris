__author__ = 'Itay'

class CodeWriter:
    def __init__(self, file):
        """
        Opens the output file/stream and gets ready to write into it.
        """
        self.file = open(file, 'w')

    def setFileName(self, fileName):
        """
        Informs the code writer that the translation of a new VM file is started.
        """
        self.file = open(fileName)

    def writeArithmetic(self, command):
        """
        Writes the assembly code that is the  translation of the given arithmetic command.
        """

    segmentsCodes = {"local":"LCL", "argument":"ARG", "this":"THIS", "that":"THAT", "pointer":"3", "temp":"5"}

    def translateDict(self, segment):
        return self.segmentsCodes[segment]

    def writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the  translation of the given command, where
        command is one of the two enumerated values: C_PUSH or C_POP
        """
        commandStr = ''
        print (command, segment, index)
        if command is "C_PUSH":
            print ("in push")
            if segment == ("temp" or "pointer"):
                commandStr = "@"+index +"\n" + \
                             "D=A\n" + \
                             "@"+self.translateDict(segment)+"\n"+ \
                             "A = A+D\n" + \
                             "D = M\n" + \
                             "@SP\n" + \
                             "A = M\n" + \
                             "M = D\n" + \
                             "@SP\n" +\
                             "M=M+1\n"

            elif segment == ("this" or "that" or "local" or "argument" ):
                commandStr = "@"+index +"\n" + \
                             "D=A\n" + \
                             "@"+self.translateDict(segment)+"\n"+ \
                             "A = M+D\n" + \
                             "D = M\n" + \
                             "@SP\n" + \
                             "A = M\n" + \
                             "M = D\n" + \
                             "@SP\n" +\
                             "M=M+1\n"
            elif segment == "constant": # push constant
                print ("in constant")
                commandStr = "@" + index + "\n" +\
                             "D=A\n" + \
                             "@SP\n" + \
                             "A = M\n" + \
                             "M = D\n" + \
                             "@SP\n" +\
                             "M=M+1\n"
            elif segment == "static":
                commandStr = "@"+self.file.name.split(".")[0] + "." + index + "\n" + \
                             "D = M" + \
                             "@SP\n" + \
                             "A = M\n" + \
                             "M = D\n" + \
                             "@SP\n" +\
                             "M=M+1\n"
        else: # pop
            print ("in pop")
            if segment == ("temp" or "pointer"):
                commandStr = "@" + index + "\n" + \
                             "D = A\n" + \
                             "@"+self.translateDict(segment)+"\n"+ \
                             "D = A + D\n" + \
                             "@R13\n" + \
                             "M = D\n" + \
                             "@SP\n" + \
                             "A = M\n" + \
                             "D = M\n" + \
                             "@R13\n" + \
                             "A = M\n" + \
                             "M = D\n" + \
                             "@SP\n" + \
                             "M = M - 1\n"
            elif ((segment == "local") or (segment == "that") or (segment == "this") or (segment == "argument")): #("this" or "that" or "local" or "argument" ):
                print("in local")
                commandStr = "@" + index + "\n" + \
                             "D = A\n" + \
                             "@"+self.translateDict(segment)+"\n"+ \
                             "A = M\n" + \
                             "D = A + D\n" + \
                             "@R13\n" + \
                             "M = D\n" + \
                             "@SP\n" + \
                             "A = M\n" + \
                             "D = M\n" + \
                             "@R13\n" + \
                             "A = M\n" + \
                             "M = D\n" + \
                             "@SP\n" + \
                             "M = M - 1\n"
            elif segment == "static":
                commandStr = "@SP\n" + \
                             "A = M\n" + \
                             "D = M\n" + \
                             "@"+self.file.name.split(".")[0] + "." + index + "\n" + \
                             "M = D\n" + \
                             "@SP\n" + \
                             "M = M - 1\n"
        self.file.write(commandStr)

    def close(self):
        """
        Closes the output file.
        """
        self.file.close()