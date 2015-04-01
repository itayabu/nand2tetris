__author__ = 'Gil'

import Parser
import Code
import SymbolTable
import sys

def main():

    inputfile = open(sys.argv[1])
    name = (inputfile.name.split('.'))[0]
    outputfile = open(name+'.hack','w')

    # Creating relevant Modulus
    parse = Parser.Parser(inputfile)
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
        parse.advance()
        if parse.commandType() is "C_COMMAND":
            binLine = '1' + code.comp(parse.comp()) + code.dest(parse.dest()) + code.jump(parse.jump())
        if parse.commandType() is "A_COMMAND":
            if parse.symbol().isnumeric():
                binLine = code.binary(parse.symbol())
            else:
                if not sym.contains(parse.symbol()):
                    sym.addEntry(parse.symbol(), sym.getNextAdd())
                binLine = code.binary(sym.getAddress(parse.symbol()))
        if parse.commandType() is "L_COMMAND":
            continue

        outputfile.write(binLine + "\n")

if __name__ == "__main__":
    main()
