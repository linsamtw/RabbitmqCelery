
import os, sys
PATH = '/'.join( os.path.abspath(__file__).split('/')[:-1] )
sys.path.append(PATH)
from Tasks import add
add.delay(0,0)


