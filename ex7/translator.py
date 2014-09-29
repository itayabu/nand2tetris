__author__ = 'Itay'

import Parser
import CodeWriter
import sys

def main():
    #TODO: check if input is a folder
    inputFile = sys.argv[1]
    parse = Parser.Parser(inputFile)
    outputFile = inputFile.split('.')[0] + ".asm"
    code = CodeWriter.CodeWriter(outputFile)

    while parse.hasMoreCommands():
        line = parse.advance().split(" ")
        print (parse.commandType(), line[1], line[2])
        code.writePushPop(parse.commandType(), line[1], line[2])
    code.close()


if __name__ == "__main__":
    main()
