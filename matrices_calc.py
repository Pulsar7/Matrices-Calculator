"""
Author: Benedikt Fichtner
Python-Version: 3.8.10
Matrices Calculator
"""
import math,random,sys
from rich import (pretty,console as cons)


class Calculator():
    def __init__(self,console) -> None:
        (self.console) = (console)
    
    def __call__(self) -> None:
        inp_matrix_a = self.console.input("Matrix A> ")
        inp_matrix_b = self.console.input("Matrix B> ")
        matrix_a:list[int] = []
        matrix_b:list[int] = []
        for arg in inp_matrix_a:
            if arg != "[" and arg != "]" and arg != ",":
                matrix_a.append()


#
pretty.install()
console = cons.Console()
#

if __name__ == '__main__':
    calc = Calculator(console = console)
    calc()