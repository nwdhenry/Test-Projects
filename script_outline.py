# This script generates outlines of Python files by extracting information about classes, methods, assignments, and imports.
# The outlines are saved in a text file called outlines.txt.
#
# The purpose of generating outlines for code is to make it easier to communicate the structure of the code to an AI system with limits in memory or history. 
# This can be particularly useful when working with large and complex codebases that are impossible to process as a whole. 
# Additionally, some IDEs like VSCode or Visual Studio do not allow for easy outline export, so generating outlines using this script can be a helpful workaround.
# 
# The get_outline function takes a filename as input and returns a list of tuples representing the outline of the file.
# Each tuple contains two elements: a string indicating the type of the code element (class, method, assignment, or import),
# and a string containing the actual code element.
#
# The main function loops through all the Python files in the current directory (excluding itself),
# calls the get_outline function for each file, and saves the outlines in outlines.txt.
#
# Note: This script assumes that the code follows certain conventions, such as using indentation to indicate scope.
# It may not work properly with all Python code. 

import os

def get_outline(file):
    # initialize some flags
    outline = []  # this will hold the outline of the file
    in_class = False  # flag to indicate whether we are currently in a class definition
    in_method = False  # flag to indicate whether we are currently in a method definition
    in_assignment = False  # flag to indicate whether we are currently in an assignment statement
    capture_variables = True  # flag to indicate whether we are currently capturing variables or not

    # open the file for reading
    with open(file, 'r', encoding='utf-8') as f:
        # iterate over each line in the file
        for line in f:
            stripped = line.strip()
            # check if the line starts with 'class'
            if stripped.startswith('class '):
                # If we encounter a new class, we set capture_variables to True again
                in_class = True
                outline.append(('class', stripped))
                capture_variables = True
            # check if the line starts with 'def __init__'
            elif stripped.startswith('def __init__'):
                # If we encounter a new method, we set in_method to True and capture_variables to False
                in_method = True
                outline.append(('method', stripped))
                capture_variables = True
            # check if the line starts with 'def ' but is not indented (i.e. not inside a method)
            elif stripped.startswith('def ') and not in_assignment:
                # If we encounter a new method that is not indented, we set in_method to True and capture_variables to False
                in_method = True
                outline.append(('method', stripped))
                capture_variables = False
            # check if the line is an assignment statement inside a class
            elif in_class and ' = ' in stripped:
                if in_method and stripped.startswith('self.'):
                    # if the assignment is inside a method, we only capture the variable name
                    assignment = stripped.split('=')[0].strip()
                    if '(' in assignment:
                        assignment = assignment.split('(')[0].strip()
                    if capture_variables:  # Only capture the variable if capture_variables is True
                        outline.append(('assignment', assignment))
                    # check if the assignment statement continues on the next line
                    if not stripped.endswith(')') and not stripped.endswith(']') and not stripped.endswith('}'):
                        in_assignment = True
                elif not in_method:
                    # if the assignment is outside a method, we only capture the variable name
                    assignment = stripped.split('=')[0].strip()
                    if '(' in assignment:
                        assignment = assignment.split('(')[0].strip()
                    if capture_variables:  # Only capture the variable if capture_variables is True
                        outline.append(('assignment', assignment))
                    # check if the assignment statement continues on the next line
                    if not stripped.endswith(')') and not stripped.endswith(']') and not stripped.endswith('}'):
                        in_assignment = True
            # check if we are inside an assignment statement that spans multiple lines
            elif in_assignment:
                if stripped.endswith(')') or stripped.endswith(']') or stripped.endswith('}'):
                    # if we have reached the end of the assignment statement, reset the flag
                    in_assignment = False
            # check if the line is an import statement or a magic method
            elif stripped.startswith('import ') or stripped.startswith('from ') or (stripped.startswith('__') and stripped.endswith('__')):
                outline.append(('import', stripped))
    return outline

def main():
    # Create an empty dictionary to store the outlines of each Python file
    outlines = {}

    # Loop through all the files in the current directory that end with '.py' and are not this script
    for file in os.listdir():
        if file.endswith('.py') and file != os.path.basename(__file__):
            # Call the get_outline function to generate the outline of the file, and store it in the outlines dictionary
            outlines[file] = get_outline(file)

    # Open a new file called 'outlines.txt' in write mode, and use the utf-8 encoding
    with open('outlines.txt', 'w', encoding='utf-8') as f:
        # Loop through the outlines dictionary, which contains the outlines of all the Python files
        for file, outline in outlines.items():
            # Write the filename to the file, followed by a colon
            f.write(f'{file}:\n')
            # Loop through the outline, which is a list of tuples, where each tuple contains the type of code and the code itself
            for kind, line in outline:
                # If the kind is 'class', write the line with four spaces of indentation
                if kind == 'class':
                    f.write(f'    {line}\n')
                # If the kind is 'method', write the line with eight spaces of indentation
                elif kind == 'method':
                    f.write(f'        {line}\n')
                # If the kind is 'assignment', write the line with twelve spaces of indentation
                elif kind == 'assignment':
                    f.write(f'            {line}\n')
                # If the kind is 'import', write the line with four spaces of indentation
                elif kind == 'import':
                    f.write(f'    {line}\n')
            # Write a new line after each file's outline
            f.write('\n')

if __name__ == '__main__':
    main()
