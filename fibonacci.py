## ASSIGNMENT 2:
    ## For all functions in a given file, find all outgoing method calls and sum them 
    ## fibonacci.py example: fibonacci, 2, ['fibonacci', 'fibonacci'], lucas, 2, ['lucas', 'lucas']
    
import ast
import sys
import os
import collections, functools, operator, glob
from collections import defaultdict

class ComplexityComputerVisitor(ast.NodeVisitor):
    """

        Evaluate the complexity of functions in a Python program
        (Example written in class)

        Complexity of a function is defined in this
        program as being the "number of if conditionals
        in the program"

        Please think about how to refine it.


        computing complexity of all the python files in
        the airflow folder for example:

            find airflow -name "*.py" | xargs -L 1 python complexity_visitor.py > airflow-analysis.csv

        sorting the outputs based on their complexity:

            cat airflow-analysis.csv | sort --field-separator=',' --key=3 -n

        should result in something like this:

            airflow/airflow/contrib/hooks/spark_jdbc_hook.py, _build_jdbc_application_arguments, 14
            airflow/airflow/gcp/hooks/bigquery.py, run_load, 16
            airflow/airflow/gcp/hooks/bigquery.py, run_query, 17
            airflow/airflow/gcp/operators/spanner.py, _validate_inputs, 18
            airflow/airflow/contrib/hooks/spark_submit_hook.py, _build_spark_submit_command, 25

        surely, you would get different results with a more intelligent
        implementation of the complexity

    """

    def __init__(self):
        self.function_complexity = dict()
        self.current_function = ""
        self.imports = dict()
        self.importFs = dict()
        self.fanout = defaultdict(list)

    def compute_complexity(self, node):
        self.visit(node)
        
        return (complexity_visitor.imports.items(), complexity_visitor.importFs.items())
        #return complexity_visitor.function_complexity.items()
    
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
        
    def visit_Call(self, call_):
        if self.fanout.get(self.current_function):
            #self.fanout[self.current_function] += 1
            #HOW TO GET NAME OF THE FUNCTION WE ARE CALLING???
            # how to add to list https://stackoverflow.com/questions/26367812/appending-to-list-in-python-dictionary
            self.fanout[self.current_function].append(self.current_function)
        else: 
            self.fanout[self.current_function].append(self.current_function)
        #print(call_)
        #print(self.current_function)
        
        self.generic_visit(call_)
        
 
list_of_files = ["C:\\Users\\grunb\\UniversityProjects\\Files\\fibonacci.py"]

    
complexity_visitor = ComplexityComputerVisitor()
    
for file_name in list_of_files:
    f = open(file_name)
    func_ast = ast.parse(f.read())
    fanouts = complexity_visitor.compute_fanout(func_ast)
    
for fun, fo in fanouts:
    print(fun+", "+str(fo)) # MAKE A LIST of call names and print it