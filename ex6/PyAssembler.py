__author__ = 'Gil'

import Parser
import Code
import sys

def main():
    print("hello world")
    inputfile = open(sys.argv[1])
    name = (inputfile.name.split('.'))[0]
    parse = Parser.Parser(inputfile)
    code = Code.Code()
    print(parse.lines)
    print(parse.advance())
    print(parse.dest())
    print(parse.comp())
    print(parse.jump())
    print(code.dest(parse.dest()))
    print(code.comp(parse.comp()))
    print(code.jump(parse.jump()))
    print(parse.commandType())
    print(parse.advance())
    print(parse.dest())
    print(parse.jump())
    print(parse.advance())
    print(parse.symbol())
    # while parse.hasMoreCommands():
    #     print(parse.advance())


    ##line = inputfile.readline()

    outputfile = open(name+'.hack','w')
    outputfile.write("hello\n")
if __name__ == "__main__":
    main()
