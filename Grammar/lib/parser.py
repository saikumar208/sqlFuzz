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
        return re.compile(r'--h3(.*?)--/h3', re.DOTALL)

    @staticmethod
    def getExprRegex():
        return re.compile(r'\n<(.*?)>(\s)*::=(.*?)(``)', re.DOTALL)

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

    def createTokens(self, expressions ):
        for i, exp in enumerate( expressions ):
            if i == 0:
                ''' To account for initial statement '''
                tokenName = "SQL terminal character"
                exp = exp.replace(tokenName, "")
            else:
                tokenName = exp.pop(0)
            tokenName = tokenName.replace(" ", "_")
            #members = "".join(exp)
            members = re.sub(r"(\t|\n|``)*", "", members )
            print( members )

    def parse(self):
        ''' Read Grammar and Create Tokens '''

        grammar = self.readGrammar()
        grammar = self.cleanGrammarFile( grammar )
        validExpressions = self.extractExpressions( grammar )

        self.createTokens( validExpressions )


a = Parser()
a.parse()