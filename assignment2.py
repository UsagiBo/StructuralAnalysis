## ASSIGNMENT 2:
    ## For all functions in a given file, find all outgoing method calls and sum them 
    ## fibonacci.py example: fibonacci, 2, ['fibonacci', 'fibonacci'], lucas, 2, ['lucas', 'lucas']
    
import ast
import sys
import os
import collections, functools, operator, glob
from collections import defaultdict

class ComplexityComputerVisitor(ast.NodeVisitor):

    def __init__(self):
        self.function_complexity = dict()
        self.current_function = ""
        self.imports = dict()
        self.importFs = dict()
        self.fanout = defaultdict(list)

    def compute_complexity(self, node):
        self.visit(node)
        return complexity_visitor.function_complexity.items()
    
    def compute_fanout(self, node):
        self.visit(node)
        return complexity_visitor.fanout.items()

    def _indent(self, code):
        return (" " * self.indent) + code

    def visit_FunctionDef(self, fundef):
        self.current_function = fundef.name

        self.generic_visit(fundef)

        self.current_function = ""

    def visit_If(self, if_):
        if self.function_complexity.get(self.current_function):
            self.function_complexity[self.current_function] += 1
        else:
            self.function_complexity[self.current_function] = 1

        self.generic_visit(if_)
        
    def visit_While(self, while_):
        if self.function_complexity.get(self.current_function):
            self.function_complexity[self.current_function] += 2
        else:
            self.function_complexity[self.current_function] = 2
        
        self.generic_visit(while_)
    
    def visit_Import(self, import_):
        for imports in import_.names:
            if(self.imports.get(imports.name)):
                self.imports[imports.name] += 1
            else:
                self.imports[imports.name] = 1
                
        self.generic_visit(import_)
        
    def visit_ImportFrom(self, importFrom_):
        for imports in importFrom_.names:
            if(self.importFs.get(imports.name)):
                self.importFs[imports.name] += 1
            else:
                self.importFs[imports.name] = 1
                
        self.generic_visit(importFrom_)
        
        
# Does not work correctly as it is appending the calling function name rather than the name of the function being called
# We are not sure how to get the name of the called function
    def visit_Call(self, call_):
        if self.fanout.get(self.current_function):
            self.fanout[self.current_function].append(self.current_function)
        else: 
            self.fanout[self.current_function].append(self.current_function)
        
        self.generic_visit(call_)

        

## hardcoded path with test file, replace this with whatever to be analysed, use glob to read multiple files at once
list_of_files = ["C:\\Users\\grunb\\UniversityProjects\\Files\\fibonacci.py"]
    
complexity_visitor = ComplexityComputerVisitor()
    
for file_name in list_of_files:
    f = open(file_name)
    func_ast = ast.parse(f.read())
    fanouts = complexity_visitor.compute_fanout(func_ast)
    
for fun, fo in fanouts:
    print(fun+", "+str(fo))

    