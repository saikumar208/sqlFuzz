"""
File to parse bnf Grammar
"""

from config.grammarConfig import GRAMMAR_FILE
from config.generalConfig import getAbsPath
import re

class BNF_Regex():

    def __init__(self):
        ''' initialize '''

    @staticmethod
    def getCommentRegex():
        ''' Regex for comment '''
        return re.compile(r'--p(.*?)--/p', re.DOTALL)

    @staticmethod
    def getHtmlHeaderRegex():
        ''' Regex for comment '''
        return re.compile(r'(--h(\d)(.*?)--/h(\d))|(--hr)|(See the Syntax Rules.)', re.DOTALL)

    @staticmethod
    def getExprRegex():
        return re.compile(r'\n<(.*?)>(\s)*::=(.*?)(``)', re.DOTALL)

    @staticmethod
    def getTokenCleanRegex():
        ''' Removes leading and trailing spaces, endline and `` '''
        return re.compile(r'(^(\s)*|(\s)*$|``|\n)')

    @staticmethod
    def getSplitExprRegex():

        return re.compile("((\s\s)|(\n)|\t)")

    @staticmethod
    def getCleaningRegexes():
        ''' return list of regexes that are replaced with empty string '''
        comments = BNF_Regex.getCommentRegex()
        htmlH3Header = BNF_Regex.getHtmlHeaderRegex()

        return [comments, htmlH3Header]

class Token():

    instances = dict()

    def __init__(self, **kwargs):
        self.params = kwargs
        self.name = self.params.get( "name" )
        self.members = self.params.get( "members" )
        Token.instances[ self.name ] = self

    def getMembers(self):
        ''' returns Members '''

        return self.members

class Parser():

    def __init__(self):
        ''' Initialize Class '''
        self.filePath = getAbsPath( GRAMMAR_FILE )

    def openFile(self):
        ''' Open Grammar File'''
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
        ''' read Grammar '''

        grammarFile = self.openFile()

        grammar = grammarFile.read()

        return grammar

    def cleanGrammarFile(self, grammar ):
        ''' removes unnecessary text from grammar '''
        for regEx in BNF_Regex.getCleaningRegexes():
            grammar = regEx.sub( "", grammar )
        return grammar

    def extractExpressions(self, grammar ):
        ''' Extract Expressions from grammar '''
        validExpressions = BNF_Regex.getExprRegex().findall(self.prepGrammarForParsing(grammar))
        validExpressions = ["".join(x) for x in validExpressions]
        return validExpressions

    def cleanExpressionList(self, expList ):
        '''removes useless statements '''
        expList = [ re.sub(r'(\t|\n|^(\s)*$|``)', '', x) for x in expList if x is not None ]
        expList = [ re.sub(r'<\s*>', '_', x) for x in expList if x != '' ]
        return expList

    def createTokens(self, expressions ):
        for i, exp in enumerate( expressions ):
            exp = BNF_Regex.getSplitExprRegex().split( exp )
            tokenName = exp.pop(0)
            exp = self.cleanExpressionList( exp )
            tokenName = tokenName.replace(" ", "_")
            assignment = ''.join(exp)
            members = BNF_Regex.getTokenCleanRegex().sub("", assignment)
            print( tokenName, members )

    def parse(self):
        ''' Read Grammar and Create Tokens '''

        grammar = self.readGrammar()
        grammar = self.cleanGrammarFile( grammar )
        validExpressions = self.extractExpressions( grammar )

        self.createTokens( validExpressions )


a = Parser()
a.parse()