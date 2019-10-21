## ASSIGNMENT 1:

## ComplexityVisitor: we measure the complexity of a given file or files by summing up all imports and import froms from the files
    ## this provides an overview of the most and least used libraries

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

    def compute_complexity(self, node):
        self.visit(node)
        return (complexity_visitor.imports.items(), complexity_visitor.importFs.items())

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
        
    def visit_Call(self, call_):
        if self.fanout.get(self.current_function):
            self.fanout[self.current_function].append(self.current_function)
        else: 
            self.fanout[self.current_function].append(self.current_function)
        
        self.generic_visit(call_)
        

## for testing purposes:
##list_of_files = ["C:\\Users\\grunb\\UniversityProjects\\Files\\fibonacci.py"]

list_of_files = []

for file in glob.glob("C:\\Users\\grunb\\UniversityProjects\\Files\\all\\*"):
    list_of_files.append(file)
    
print("Summing up import statements in the following " + str(len(list_of_files)) + " files:")
for file in list_of_files:
    print("- " + os.path.basename(file))
    
complexity_visitor = ComplexityComputerVisitor()
    
for file_name in list_of_files:
    f = open(file_name)
    func_ast = ast.parse(f.read())
    importVals, importFVals = complexity_visitor.compute_complexity(func_ast)
    
for fun, complexity in importVals:
    print("IMPORT " + fun + ", count: " + str(complexity))

for fun, complexity in importFVals:
    print("IMPORT FROM " + fun + ", count: " + str(complexity))
    