__author__ = 'Gil'

import Parser
import Code
import SymbolTable
import sys
import os


def main():

    userInput = sys.argv[1]

    #Case input is a directory, run on each .asm file and parse it
    if os.path.isdir(userInput):
        if not userInput.endswith("/"):
            userInput += "/"
        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.asm'):
                parseFile(userInput+file)
    #Case input is file, just parse it
    elif os.path.isfile(userInput):
        parseFile(userInput)
    #Raise an exception
    else:
        raise Exception("The input is not valid, please try again")

#Parsing a file by a given path
def parseFile(path):
    inputFile = open(path)
    name = (inputFile.name.split('.'))[0]
    outputFile = open(name+'.hack', 'w')

    #Creating relevant Modulus
    parse = Parser.Parser(inputFile)
    code = Code.Code()
    sym = SymbolTable.SymbolTable()

    #First Run
    #Inserts 'L Commands' to the symbolTable
    while parse.hasMoreCommands():
        parse.advance()
        if parse.commandType() is "L_COMMAND":
            sym.addEntry(parse.symbol(), parse.lineCount - 1)
            parse.deleteLine()
    parse.resetCommands()

    #Second Run
    #Translate each command line to binary code
    while parse.hasMoreCommands():
        #binLine = ''
        parse.advance()
        if parse.commandType() is "C_COMMAND":
            binLine = '1' + code.comp(parse.comp()) + code.dest(parse.dest()) + code.jump(parse.jump())
        if parse.commandType() is "A_COMMAND":
            if parse.symbol().isnumeric():
                binLine = code.binary(parse.symbol())
            else: #commandType is L_COMMAND
                if not sym.contains(parse.symbol()):
                    sym.addEntry(parse.symbol(), sym.getNextAdd())
                binLine = code.binary(sym.getAddress(parse.symbol()))
        if parse.commandType() is "L_COMMAND":
            continue

        outputFile.write(binLine + "\n")

    outputFile.close()

if __name__ == "__main__":
    main()
