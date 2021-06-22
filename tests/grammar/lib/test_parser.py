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
        for x in Token._instances:
            print(x)
            token = Token.getTokenByName( x )
            exceptions = ['bitstringliteral', 'hexstringliteral', 'initialalphabeticcharacter',
                          'ideographiccharacter', 'whitespace', 'slash', 'unqualifiedschemaname',
                          'numericvalueexpressiondividend', 'numericvalueexpressiondivisor', 'tableborder=1',
                          'th', '/th', 'pre', 'sup', '/sup', '/pre', 'tr', 'td', '/td', '/tr', '/table',
                          'character--@@setspecification', 'handlerdeclaration']
            if token.name in exceptions:
                continue
            print(token)

            for val in token.values:
                print( val )
                if token.isToken( val ):
                    Token.getTokenByName( val )
                    assert( Token.getInstanceKeyByName( val ) in Token._instances )
