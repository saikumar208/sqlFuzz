''' Contains general Config '''

import os

HOME_DIR_PATH = r"C:\Users\Sai\PycharmProjects\sqlFuzz" # fix this

def getAbsPath( relPath ):
    ''' Return Absolute Path '''
    path = os.path.join(HOME_DIR_PATH, relPath)
    return path
