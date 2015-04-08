__author__ = 'Itay'

import Parser
import CodeWriter
import sys
import os

def translateFile(file, code):
    parse = Parser.Parser(file)
    while parse.hasMoreCommands():
        parse.advance()
        if parse.commandType() == "C_PUSH" or parse.commandType() == "C_POP":
            code.writePushPop(parse.commandType(), parse.arg1(), parse.arg2())
        elif parse.commandType() == "C_ARITHMETIC" :
            code.writeArithmetic(parse.currCommand)
        elif parse.commandType() == "C_GOTO":
            code.writeGoto(parse.arg1())
        elif parse.commandType() == "C_IF":
            code.writeIf(parse.arg1())
        elif parse.commandType() == "C_LABEL":
            code.writeLabel(parse.arg1())
        elif parse.commandType() == "C_RETURN":
            code.writeReturn()
        elif parse.commandType() == "C_FUNCTION":
            code.writeFunction(parse.arg1(), parse.arg2())
        elif parse.commandType() == "C_CALL":
            code.writeCall(parse.arg1(), parse.arg2())
        else:
            print("error in translateFile")

def main(argv):
    userInput = sys.argv[1]

    if os.path.isdir(userInput):
        if userInput.endswith("/"):
            userInput = userInput[0:-1]
        dirname = os.path.basename(userInput)
        outputFile = userInput + "/" + dirname + ".asm"
        code = CodeWriter.CodeWriter(outputFile)
        code.writeInit()
        for file in os.listdir(userInput):
            if ".vm" in file.lower():
                code.setFileName(file)
                translateFile(userInput + "/" + file, code)
    else:
        outputFile = userInput.split('.')[0] + ".asm"
        code = CodeWriter.CodeWriter(outputFile)
        code.setFileName(userInput)
        translateFile(userInput, code)

if __name__ == "__main__":
    main(sys.argv)