
import re
from lib.grammar.regexes import BNF_Regex

# RHSExpParser is a parser element but is declared here to avoid circular references

class LexElementMaster():

    _map = dict()

    def __init__(self, **kwargs):
        pass

class LexElementbase():

    @staticmethod
    def formatLexName(name):
        ''' Formats token name the way it is stored in instances'''
        # Does not remove angular brackets

        name = re.sub(r"(\s)", "", name)
        name = re.sub('<|>', '', name)
        name = re.sub('\s', '', name)
        name = BNF_Regex.getTrailingUnderscore().sub("", name)
        return name

    @staticmethod
    def getInstanceKeyByName(name):
        name = Token.formatLexName(name)
        name = re.sub(r"(<|>)", "", name)
        return name

    @staticmethod
    def getLexElemByName(clazz, name):
        ''' return Token by name '''
        fmtName = clazz.getInstanceKeyByName(name)
        # if Token.isToken( name ):
        return clazz._instances[fmtName]

class RHSExpParser():

    def __init__(self, **kwargs):
        ''' Creates relevant Lex element '''
        self.params = kwargs
        self.name = self.params.get("name")
        if len(self.name) > 0:
            self.fmtName = BNF_Regex.getLeadingNTrailingSpaces().sub( "", self.name )
            isToken = self.tokenCheck()
            isExpression = self.expressionCheck()
            isAtom = self.isAtom()
            self.isValidLexObj([ isToken, isExpression, isAtom ])
            self.createLexObj(isToken, isExpression, isAtom)


    def createLexObj(self, isToken, isExpression, isAtom):
        if isToken:
            Token( **self.params )
        elif isExpression:
            Expression( **self.params )
        elif isAtom:
            AtomicLiteral( **self.params )

    def isValidLexObj(self, testRes):
        if sum(testRes) == 1:
            return True
        return False

    def tokenCheck(self):
          # remove leading and trailing spaces
        if Token.isToken( self.fmtName ):
            if "values" in self.params:
                if not len(self.params.get( "values" )) > 2:
                    return False
                else:
                    return True
            else:
                return True
        return False

    def isAtom(self):
        ''' Checks if lex element is an atom'''
        if not Token.isToken( self.name ) and len(self.params.get( "values", "" )) <= 2:
            if AtomicLiteral.isAtomicLiteral( self.name ):
                return True
        return False

    def expressionCheck(self):
        ''' checks if a given expression is an expression '''
        # Currently similar to token check
        if not self.fmtName.startswith("<") and ( self.fmtName not in Token._instances ) and ( len(self.fmtName) > 1 ):
            return True
        return False

class Expression( LexElementbase ):

    _instances = dict()

    def __init__(self, **kwargs):
        self.params = kwargs
        self.name = self.params.get( "name" )
        self.members = self.params.get( "values" )   # To keep params same as in Tokens
        Expression._instances[ self.name ] = self
        self.initMembers()

    def __str__(self, *args, **kwargs):

        return self.members

    def getMembers(self):
        ''' returns Members '''

        return self.values

    def initMembers(self):
        print(self.params)
        pass


class AtomicLiteral( LexElementbase ):

    _instances = dict()

    def __init__(self, **kwargs):
        self.params = kwargs
        self.name = self.formatLexName( self.params.get("name") )
        self.value = self.params.get( "values" )
        AtomicLiteral._instances[ self.name ] = self

    @staticmethod
    def isAtomicLiteral( name ):
        bool1 = not( name.startswith("<") and name.endswith(">") )  # token must start and end with ang brackets
        bool2 = (name.count('<') == 0 and name.count('>') == 0)  # there must be only one pair
        bool3 = name.count("[") == 0
        if all([bool1, bool2, bool3]):  # or name in Token._instances:
            return True
        return False

class Token( LexElementbase ):

    _instances = dict()

    def __init__(self, **kwargs):

        name = kwargs.get("name")
        self.name = self.formatLexName(name)
        if self.name in Token._instances:
            Token._instances[ self.name ].params.update(kwargs)
            self.params = Token._instances[ self.name ].params
            del Token._instances[ self.name ]   # easy way to get rid of old instance
            #kwargs.update( Token._instances[name].params )
        else:
            self.params = kwargs


        self.setValues()
        self.isAtom = self.params.get( "isAtom", False )
        self.isReqArg = self.params.get( "isReq", False )
        Token._instances[ self.name ] = self


    def __str__(self, *args, **kwargs):

        return "%s %s"%( self.name, str(self.values ) )

    @staticmethod
    def getValidTokens():

        return Token._instances.keys()

    @staticmethod
    def isToken( name ):
        ''' Checks if a given name is a token '''
        bool1 = name.startswith("<") and name.endswith(">") #token must start and end with ang brackets
        bool2 = (name.count('<') == 1 and name.count('>') == 1) # there must be only one pair
        bool3 = name.count("[") == 0
        if all([bool1, bool2, bool3]):# or name in Token._instances:
            return True
        return False

    @staticmethod
    def getTokenByName( name ):
        ''' return Token by name '''
        return Token.getLexElemByName( Token, name )

    def setValues( self ):
        values = self.params.get( "values", None )

        if values is not None:
            Token.breakDownExp(values)
            self.values = [Token.formatLexName(x) for x in values.split("|")]
            pass

    def updateValuesType( self ):
        ''' Once all tokens have been created, update the types of the tokens '''
        pass

    def getValues(self):
        ''' yield values '''
        for token in self.values:
            yield  token

    @staticmethod
    def breakDownExp( expression ):
        ''' breaks down expressions into individual tokens '''

        if expression is None:
            return

        expressions = expression.split( "|" )

        _ = [ RHSExpParser(**{'name': x}) for x in expressions ]
        # First create tokens enclosed in <>
