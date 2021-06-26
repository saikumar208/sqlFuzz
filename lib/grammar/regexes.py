
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

    @staticmethod
    def getLeadingNTrailingSpaces():
        return re.compile( "(^(\s)*|(\s)*$)" )