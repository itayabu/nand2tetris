__author__ = 'Itay'

import Parser
import CodeWriter
import sys
import os

def translateFile(file, code):
    parse = Parser.Parser(file)
    while parse.hasMoreCommands():
        parse.advance()
        if parse.commandType() is "C_PUSH" or parse.commandType() is "C_POP":
            code.writePushPop(parse.commandType(), parse.arg1(), parse.arg2())
        else:
            code.writeArithmetic(parse.currCommand)

def main(argv):
    userInput = sys.argv[1]

    if os.path.isdir(userInput):
        if userInput.endswith("/"):
            userInput = userInput[0:-1]
        dirname = os.path.basename(userInput)
        outputFile = userInput + "/" + dirname + ".asm"
        code = CodeWriter.CodeWriter(outputFile)
        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.vm'):
                code.setFileName(file)
                translateFile(userInput + "/" + file, code)
                code.close()
    else:
        outputFile = userInput.split('.')[0] + ".asm"
        code = CodeWriter.CodeWriter(outputFile)
        translateFile(userInput, code)
        code.close()

if __name__ == "__main__":
    main(sys.argv)
