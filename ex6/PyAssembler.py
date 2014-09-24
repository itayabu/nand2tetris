import Parser
import sys
__author__ = 'Itay'

def main():
    print("hello world")
    inputfile = open(sys.argv[1])
    name = (inputfile.name.split('.'))[0]
    parse = Parser.Parser(inputfile)
    # print(parse.hasMoreCommands())
    # print(parse.advance())
    # print(parse.lineCount)
    # print(parse.hasMoreCommands())
    # print(parse.advance())
    # print(parse.lineCount)
    # print(parse.hasMoreCommands())
    # print(parse.advance())
    # print(parse.lineCount)
    # print(parse.hasMoreCommands())
    # print(parse.lineCount)
    while parse.hasMoreCommands():
        print(parse.advance())


    ##line = inputfile.readline()


if __name__ == "__main__":
    main()
