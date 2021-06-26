''' Generates stub of SQL queries '''

from lib.grammar.parser import Parser, Token

def initializeGrammarElements():
    ''' Intializes Tokens and other elements '''

    parserObj = Parser()
    parserObj.parse()

def getExp( startingToken ):

    stack = list()
    for possibleExp in startingToken.getValues():
        print(possibleExp)
        stack.append( getExp(possibleExp) )

    return stack


#def walkGrammar():
initializeGrammarElements()
startingPoint = "preparableSQLdatastatement"
startingToken = Token.getTokenByName(startingPoint)
getExp( startingToken )
