''' Generates stub of SQL queries '''

from lib.grammar.parser import Parser, Token
from lib.grammar.grammarElements import LexElementMaster, Expression, unpack, AtomicLiteral

def initializeGrammarElements():
    ''' Intializes Tokens and other elements '''

    parserObj = Parser()
    parserObj.parse()

def getExp( startingToken ):

    level = list()
    for possibleExp in startingToken.getValues():
        print(possibleExp, type(possibleExp))
        level.append(LexElementMaster.getLexElemByNameOverride(possibleExp))

    return level

def getOptions( stack, startingToken ):
    stack.append(getExp(startingToken))
    level = stack[-1]
    for x in level:
        print( x.getValues() )
        values = x.getValues()
        qstr = []
        for val in values:
            obj = LexElementMaster.getLexElemByNameOverride(val)
            if obj is None:
                qstr += [ val ]
            else:
                if isinstance(obj, Expression):
                    actExp = obj.members




#def walkGrammar():

initializeGrammarElements()
startingPoint = "preparableSQLdatastatement"
startingToken = Token.getTokenByName(startingPoint)
print("#"*20)
stack = list()
#getOptions( stack, startingToken )
def genQuery( query, queryStruct ):

    if isinstance(queryStruct, str):
        return query + " " + queryStruct
    for x in queryStruct:
        return genQuery(query, x)

unpackedOptions =  unpack( startingToken.getValues() )

def walk( root ):

    q = ['']
    for x in root:
        if isinstance(x, str):
            newQ = []
            for y in q:
                newQ.append( y + ' ' + x)
            q = newQ
        elif isinstance(x, list):
            newQ = []
            for y in walk( x ) + ['']:
                for z in q:
                    newQ.append(z + ' ' + y)
            q = newQ
    return q

walk(unpackedOptions[0][0])         # Clean this up