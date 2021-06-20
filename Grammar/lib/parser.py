"""
Tests: tests/grammar/lib/test_parser.py
File to parse bnf Grammar
"""

from config.grammarConfig import GRAMMAR_FILE
from config.generalConfig import getAbsPath
import re
from logging import getLogger

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
    def getTokenFromExpRegex():
        return re.compile( r'<.*?>' )

    @staticmethod
    def getSplitExprRegex():

        return re.compile("((\s\s)|(\n)|\t)")

    @staticmethod
    def getCleaningRegexes():
        ''' return list of regexes that are replaced with empty string '''
        comments = BNF_Regex.getCommentRegex()
        htmlH3Header = BNF_Regex.getHtmlHeaderRegex()

        return [comments, htmlH3Header]

    @staticmethod
    def getTrailingUnderscore():

        return re.compile("(^_|_$)")

class Expression():

    instances = dict()

    def __init__(self, **kwargs):
        self.params = kwargs
        self.name = self.params.get( "name" )
        self.members = self.params.get( "members" )
        Expression.instances[ self.name ] = self
        self.initMembers()

    def getMembers(self):
        ''' returns Members '''

        return self.members

    def initMembers(self):
        ''' initializes members '''
        members = self.members.split("|")
        Token.breakDownExp( self.name, self.members )
        pass

class Literal():

    def __init__(self, **kwargs):
        self.params = kwargs

class Token():

    _instances = dict()

    def __init__(self, **kwargs):

        name = kwargs.get("name")
        self.name = self.formatTokenName( name )
        if name in Token._instances:
            kwargs.update( Token._instances[name].params )

        self.params = kwargs


        self.setValues()
        self.isAtom = self.params.get( "isAtom", False )
        self.isReqArg = self.params.get( "isReq", False )
        Token._instances[ self.name ] = self

    def __str__(self, **kwargs ):

        return "%s %s"%( self.name, str(self.values ) )

    @staticmethod
    def getValidTokens():

        return Token._instances.keys()

    @staticmethod
    def formatTokenName( name ):
        ''' Formats token name the way it is stored in instances'''
        # Does not remove angular brackets
        name = re.sub(r"(\s)", "_", name )
        name = re.sub('<|>', '', name)
        name = re.sub('\s', '_', name)
        name = BNF_Regex.getTrailingUnderscore().sub("", name)
        return name

    @staticmethod
    def getInstanceKeyByName( name ):
        name = Token.formatTokenName(name)
        name = re.sub(r"(<|>)", "", name)
        return name

    @staticmethod
    def isToken( name ):
        ''' Checks if a given name is a token '''
        if (name.startswith("<") and name.endswith(">")) or name in Token._instances:
            return True
        return False

    @staticmethod
    def getTokenByName( name ):
        ''' return Token by name '''
        fmtName = Token.getInstanceKeyByName( name )
        if Token.isToken( name ):
            return Token._instances[ fmtName ]
        raise Exception( "No Token by name '%s'"%name )

    def setValues( self ):
        values = self.params.get( "values", None )
        if values is not None:
            self.values = [ Token.formatTokenName( x ) for x in values.split("|") ]
            pass

    def updateValuesType( self ):
        ''' Once all tokens have been created, update the types of the tokens '''
        pass

    def getValues(self):
        ''' yield values '''
        for token in self.values:
            yield  token

    @staticmethod
    def breakDownExp( name, expression ):
        ''' breaks down expressions into individual tokens '''

        for tok in Token.getValidTokens():
            expression = expression.replace( tok, "")
        expression = re.sub("((<(\s)*>)|[(\s)*]])", "", expression)

        # Literals
        tokens = BNF_Regex.getTokenFromExpRegex().findall( expression )

        _ = [ Token(**{'name': x}) for x in tokens ]
        # First create tokens enclosed in <>
        Token(**{"name": name, "values" : expression})


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
            Expression(**{"name": tokenName, "members": members})

    def parse(self):
        ''' Read Grammar and Create Tokens '''

        grammar = self.readGrammar()
        grammar = self.cleanGrammarFile( grammar )
        validExpressions = self.extractExpressions( grammar )

        self.createTokens( validExpressions )


if __name__ == '__main__':
    parserObj = Parser()
    parserObj.parse()
    logger = getLogger()
    logger.info("Tokens Created")


