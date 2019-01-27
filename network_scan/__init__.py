import sys
import os


fil = __file__[:__file__.rindex(os.sep)]
print(fil)
sys.path.insert(0,fil)
