from unittest import TestCase
from Grammar.lib.parser import Parser, Token

class TestParser(TestCase):
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

    def test_parse(self):
        parserObj = Parser()
        parserObj.parse()
        exceptions = []
        isDebugMode = False
        for x in Token._instances:
            print(x)
            token = Token.getTokenByName( x )
            # Need to handle some of these exceptions
            if token.name in exceptions:
                continue
            try:
                print(token)

                for val in token.values:
                    print( val )
                    if token.isToken( val ):
                        Token.getTokenByName( val )
                        assert( Token.getInstanceKeyByName( val ) in Token._instances )

            except Exception as e:
                if isDebugMode:
                    exceptions.append( token.name )
                else:
                    raise e
        print(exceptions)
