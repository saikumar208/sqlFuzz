"""
Tests: tests/lib/grammar/test_parser.py
File to parse bnf lib
"""

from config.grammarConfig import GRAMMAR_FILE
from config.generalConfig import getAbsPath
from lib.grammar.regexes import BNF_Regex
from lib.grammar.grammarElements import Token, Expression, AtomicLiteral, RHSExpParser
import re
from logging import getLogger

class Parser():

    def __init__(self):
        ''' Initialize Class '''
        self.filePath = getAbsPath( GRAMMAR_FILE )

    def openFile(self):
        ''' Open lib File'''
        file = open( self.filePath,"r")
        return file

    def prepGrammarForParsing(self, grammar):
        '''
        :param grammar:
        :return:
        inserts `` before expressions start for easy parsing
        '''
        grammar = re.sub( r"\n<", r"``\n<", grammar )
        return grammar

    def readGrammar(self):
        ''' read lib '''

        grammarFile = self.openFile()

        grammar = grammarFile.read()

        return grammar

    def cleanGrammarFile(self, grammar ):
        ''' removes unnecessary text from lib '''
        for regEx in BNF_Regex.getCleaningRegexes():
            grammar = regEx.sub( "", grammar )
        return grammar

    def extractExpressions(self, grammar ):
        ''' Extract Expressions from lib '''
        validExpressions = BNF_Regex.getExprRegex().findall(self.prepGrammarForParsing(grammar))

        finalValidExp = []
        for expr in validExpressions:
            tokenName = "<" + expr[0] + ">" #replacing the angular brackets since it is easier to identify tokens with it
            fullExp = tokenName + "".join( expr[1:] )
            finalValidExp.append(fullExp)
        #validExpressions = ["".join(x) for x in validExpressions]
        return finalValidExp

    def cleanExpressionList(self, expList ):
        '''removes useless statements '''
        expList = [ re.sub(r'(\t|\n|^(\s)*$|``)', '', x) for x in expList if x is not None ]
        expList = [ re.sub(r'<\s*>', '', x) for x in expList if x != '' ]
        return expList

    def createTokens(self, expressions ):
        for i, exp in enumerate( expressions ):
            exp = BNF_Regex.getSplitExprRegex().split( exp )
            tokenName = exp.pop(0)
            exp = self.cleanExpressionList( exp )
            tokenName = tokenName.replace(" ", "")
            assignment = ''.join(exp)
            members = BNF_Regex.getTokenCleanRegex().sub("", assignment)
            RHSExpParser(**{"name": tokenName, "values": members})

    def parse(self):
        ''' Read lib and Create Tokens '''

        grammar = self.readGrammar()
        grammar = self.cleanGrammarFile( grammar )
        validExpressions = self.extractExpressions( grammar )

        self.createTokens( validExpressions ) # Init Tokens, expressions and atomic literals
        Expression.initAllMembers()           # Init expression members


if __name__ == '__main__':
    parserObj = Parser()
    parserObj.parse()
    logger = getLogger()
    logger.info("Tokens Created")


