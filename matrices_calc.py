"""
Author: Benedikt Fichtner
Python-Version: 3.8.10
"""
import math,random,argparse,sys
from rich import (pretty,console as cons)


class Calculator():
    def __init__(self,console) -> None:
        (self.console) = (console)
    
    def __call__(self) -> None:
        pass


#
pretty.install()
console = cons.Console()
#
parser = argparse.ArgumentParser("Matrices Calculator")
parser.add_argument('-m','--matrix',help="Matrix",type=str,nargs='+',action='append')
args = parser.parse_args()

if args.matrix == None:
    parser.print_help()
    sys.exit()
#

if __name__ == '__main__':
    calc = Calculator()
    calc()