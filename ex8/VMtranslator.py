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
    input = sys.argv[1]

    if os.path.isdir(input):
        outputFile = input + ".asm"
        code = CodeWriter.CodeWriter(outputFile)
        code.writeInit()
        for file in os.listdir(input):
            code.setFileName(file)
            translateFile(input + "\\" + file, code)
    else:
        outputFile = input.split('.')[0] + ".asm"
        code = CodeWriter.CodeWriter(outputFile)
        code.writeInit()
        translateFile(input, code)

if __name__ == "__main__":
    main(sys.argv)