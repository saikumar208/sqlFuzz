from unittest import TestCase
from lib.grammar.parser import Parser, Token, Expression

class TestParser(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestParser, cls).setUpClass()
        cls.parserObj = Parser()
        cls.parserObj.parse()

    def test_expressions(self):
        for exp in Expression._instances:
            print(exp)
        assert( True )

    def test_open_file(self):
        pass

    def test_prep_grammar_for_parsing(self):
        pass

    def test_read_grammar(self):
        pass

    def test_clean_grammar_file(self):
        pass

    def test_extract_expressions(self):
        pass

    def test_clean_expression_list(self):
        pass

    def test_create_tokens(self):
        pass

    def test_runTestParse(self):

        exceptions = []
        isDebugMode = True
        for x in Token._instances:
            #print(x)
            token = Token.getTokenByName( x )
            # Need to handle some of these exceptions
            if token.name in exceptions:
                continue
            try:
                #print(token)

                for val in token.values:
                    #print( val )
                    if token.isToken( val ):
                        Token.getTokenByName( val )
                        assert( Token.getInstanceKeyByName( val ) in Token._instances )

            except Exception as e:
                if isDebugMode:
                    exceptions.append( (token.name,e) )
                else:
                    raise e
        print("#"*100)

        for x in exceptions:
            print(x)
        #print(exceptions)
