#!/usr/bin/env python3

import os
import re
import fnmatch
import mimetypes

"""
File Renamer and Replacer

This script provides functionality to rename files within a specified directory and its subdirectories.
It can also search through the content of text files to replace occurrences of a specified string (needle)
with another string (replacement) in various naming conventions such as camelCase, PascalCase, snake_case, and kebab-case.

Usage:
    The script can be run from the command line with the following arguments:
    - Directory: The path to the directory where files will be renamed.
    - Needle: The string to search for in file names and contents.
    - Replacement: The string to replace the needle with in file names and contents.
    - Dry Run: An optional flag to print out actions without making any changes.

Example:
    python rename_script.py "/path/to/directory" "oldText" "newText" --dry-run
    python rename_script.py "/path/to/directory" -n "oldText" -r "newText" --dry-run

The script also supports excluding specific directories and file extensions during the search and replace process.

Please ensure that you have backups of your files before running this script as it makes changes that cannot be undone.
"""

def to_pascal_case(kebab_str: str) -> str:
    """
    Convert a kebab-case string to PascalCase.

    Parameters:
    kebab_str (str): The kebab-case string to convert to PascalCase.

    Returns:
    str: The string converted to PascalCase format.
    """
    return ''.join(word.capitalize() for word in kebab_str.split('-'))

def to_camel_case(kebab_str: str) -> str:
    """
    Convert a kebab-case string to camelCase.

    Parameters:
    kebab_str (str): The kebab-case string to convert to camelCase.

    Returns:
    str: The string converted to camelCase format.
    """
    parts = kebab_str.split('-')
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])


def to_snake_case(s: str) -> str:
    """
    Convert a kebab-case string to snake_case.

    This function assumes that the input string is in kebab-case.

    Parameters:
    s (str): The kebab-case string to convert to snake_case.

    Returns:
    str: The string converted to snake_case format.
    """
    # Replace hyphens with underscores to convert to snake_case
    return s.replace('-', '_')


def to_kebab_case(s: str) -> str:
    """
    Convert a string from camelCase, PascalCase, snake_case, or kebab-case to kebab-case.
    Throw an error if the conversion results in consecutive hyphens.

    Parameters:
    s (str): The string to convert to kebab-case.

    Returns:
    str: The string converted to kebab-case format.

    Raises:
    ValueError: If the conversion results in consecutive hyphens.
    """
    # Replace underscores and spaces with hyphens
    s = s.replace('_', '-').replace(' ', '-')

    # Insert hyphens before uppercase letters not at the start of the string and convert to lowercase
    kebab_case_string = re.sub(r'(?<!^)(?=[A-Z])', '-', s).lower()

    # Remove potential consecutive hyphens caused by the above transformations
    kebab_case_string = re.sub(r'-+', '-', kebab_case_string)

    return kebab_case_string

def detect_case_type(string: str) -> str:
    """
    Detect the case type of a given string.

    Parameters:
    string (str): The string for which to detect the case type.

    Returns:
    str: A string indicating the detected case type.
         Possible returns are 'camelCase', 'PascalCase', 'snake_case', 'kebab-case', or 'other'.
    """
    patterns = {
        # 'snake_case': r'^[a-z]+(_[a-z]+)*$',
        # 'kebab-case': r'^[a-z]+(-[a-z]+)*$',
        # 'camelCase': r'^[a-z][a-zA-Z0-9]*$',
        # 'PascalCase': r'^[A-Z][a-zA-Z0-9]*$'
        
        # 'snake_case': r'^[a-z0-9]+(?:_[a-z0-9]+)*$',  # Allow numbers within snake_case
        # 'kebab-case': r'^[a-z]+(?:-[a-z0-9]+)*$',    # Allow numbers within kebab-case
        # 'camelCase': r'^[a-z][a-zA-Z0-9]*$',         # Lowercase first character, no underscores or hyphens
        # 'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',        # Uppercase first character, no underscores or hyphens
        
        'snake_case': r'^[a-z0-9]+(?:_[a-z0-9]+)*$',   # Lowercase or numbers, separated by underscores
        'kebab-case': r'^[a-z0-9]+(?:-[a-z0-9]+)*$',   # Lowercase or numbers, separated by hyphens
        'camelCase': r'^[a-z][a-zA-Z0-9]*$',           # Lowercase first character, followed by a mix of alphanumeric characters
        'PascalCase': r'^[A-Z][a-zA-Z0-9]*$',          # Uppercase first character, followed by a mix of alphanumeric characters

    }

    for case, pattern in patterns.items():
        if re.match(pattern, string):
            return case
    
    return 'other'


def convert_string(string: str, to_case: str) -> str:
    """
    Convert a string from its detected naming convention to another specified convention.

    Parameters:
    string (str): The string to convert.
    to_case (str): The target naming convention to convert the string to ('camelCase', 'PascalCase', 'snake_case', 'kebab-case').

    Returns:
    str: The string converted to the target naming convention.
    """
    
    kebab = to_kebab_case(string)

    # Convert the string to the target case from the detected case
    if to_case == 'camelCase':
        return to_camel_case(kebab)
    elif to_case == 'PascalCase':
        return to_pascal_case(kebab)
    elif to_case == 'snake_case':
        return to_snake_case(kebab)
    elif to_case == 'kebab-case':
        return kebab
    elif to_case == 'other':
        return string
    else:
        raise ValueError(f"Unsupported target case: {to_case}")
    
    
def generate_all_case_variations(text: str) -> dict:
    """
    Generate all case variations for a given text.

    Parameters:
    text (str): The text to generate case variations for.

    Returns:
    dict: A dictionary with keys as case types and values as the text in that case format.
    """

    # Error if string is not valid
    detect_case_type(text)
    
    kebab = to_kebab_case(text)
  
    return {
        'original': text,
        'camelCase': to_camel_case(kebab),
        'PascalCase': to_pascal_case(kebab),
        'snake_case':  to_snake_case(kebab),
        'kebab-case': kebab
    }
    

def replace_text_in_filename(filename: str, needle_variations: dict, replacement_variations: dict) -> str:
    """
    Replace text in a filename with the appropriate case format.

    Parameters:
    filename (str): The original filename.
    needle_variations (dict): All case variations of the needle text.
    replacement_variations (dict): All case variations of the replacement text.

    Returns:
    str: The new filename with the replacement text.
    """
    for case_type, needle_variation in needle_variations.items():
        if needle_variation in filename:
            return filename.replace(needle_variation, replacement_variations[case_type])
    return filename

def rename_files(directory: str, needle: str, replacement: str, exclude_dirs=None, dry_run: bool = False, ask: bool = True):
    """
    Rename files within the given directory and its subdirectories.
    It looks for the needle in any naming convention in the filenames and replaces it with the
    replacement in the same naming convention.

    Parameters:
    directory (str): The root directory from which to start renaming files.
    needle (str): The substring to look for in filenames for renaming.
    replacement (str): The substring that will replace the needle in filenames.
    exclude_dirs (list): Directories to exclude from the search.
    dry_run (bool): If True, print out the rename actions without performing them.
    ask (bool): If True, ask for confirmation before performing the replace operation.
    """
    # Verify the directory exists and is not empty
    if not os.listdir(directory):
        raise ValueError(f"The directory '{directory}' is empty or does not exist.")

    # Verify the needle is not falsy
    if not needle:
        raise ValueError("The needle must not be empty or only whitespace.")

    # Check if the replacement is falsy and ask for confirmation
    if not replacement and ask:
        confirmation = input("The replacement string is empty. This will remove the needle from filenames. Are you sure you want to continue? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation cancelled.")
            return
          
    exclude_dirs = exclude_dirs if exclude_dirs else []
          
    # Print the operation details
    abs_directory = os.path.abspath(directory)
    print(f"Directory: {abs_directory}")
    print(f"Needle: {needle}")
    print(f"Replacement: {replacement}")
    print(f"Exclude directory: {exclude_dirs}")
    print(f"Dry Run: {dry_run}")
    
    # Ask for user confirmation
    if ask:
        if dry_run:
            confirmation = input("The operation is in dry run mode. Do you want to proceed? (y/n): ")
        else:
            confirmation = input("Are you sure you want to rename files? This action cannot be undone. (y/n): ")

        if confirmation.lower() != 'y':
            print("Operation cancelled.")
            return

    # Generate all case variations for needle and replacement
    needle_variations = generate_all_case_variations(needle)
    replacement_variations = generate_all_case_variations(replacement)

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in files:
            # Replace text in the filename if needed
            new_filename = replace_text_in_filename(filename, needle_variations, replacement_variations)
            if new_filename != filename:
                original_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_filename)
                
                # Rename the file
                if (dry_run):
                    print(f'Would rename "{original_file_path}" to "{new_file_path}"')
                else:
                    try:
                        os.rename(original_file_path, new_file_path)
                        print(f'Renamed "{original_file_path}" to "{new_file_path}"')
                    except OSError as e:
                        print(f"Error renaming file {original_file_path}: {e}")

def replace_in_files(directory: str, needle: str, replacement: str, exclude_dirs=None, exclude_extensions=None, dry_run: bool = True, ask: bool = True):
    """
    Replace occurrences of needle in any format (camelCase, PascalCase, snake_case, kebab-case) within text files in a directory.
    Supports exclusions for directories, file extensions, and wildcard patterns.

    Parameters:
    directory (str): The root directory from which to start replacing text in files.
    needle (str): The substring to find in file contents for replacing.
    replacement (str): The substring to replace the needle with in file contents.
    exclude_dirs (list): Directories to exclude from the search.
    exclude_extensions (list): File extensions to exclude from the search.
    dry_run (bool): If True, print out the replace actions without performing them.
    ask (bool): If True, ask for confirmation before performing the replace operation.
    """
    
    # Verify the directory exists and is not empty
    if not os.listdir(directory):
        raise ValueError(f"The directory '{directory}' is empty or does not exist.")

    # Verify the needle is not falsy
    if not needle:
        raise ValueError("The needle must not be empty or only whitespace.")

    # Check if the replacement is falsy and ask for confirmation
    if not replacement and ask:
        confirmation = input("The replacement string is empty. This will remove the needle from filenames. Are you sure you want to continue? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation cancelled.")
            return
                
    # Ask for user confirmation
    if ask:
        if dry_run:
            confirmation = input("The operation is in dry run mode. Do you want to proceed? (y/n): ")
        else:
            confirmation = input("Are you sure you want to replace inside files? This action cannot be undone. (y/n): ")

        if confirmation.lower() != 'y':
            print("Operation cancelled.")
            return

    # Generate all case variations for needle and replacement
    needle_variations = generate_all_case_variations(needle)
    replacement_variations = generate_all_case_variations(replacement)

    exclude_dirs = exclude_dirs if exclude_dirs else []
    exclude_extensions = exclude_extensions if exclude_extensions else []

    # Print the operation details
    abs_directory = os.path.abspath(directory)
    print(f"Directory: {abs_directory}")
    print(f"Needle: {needle}")
    print(f"Replacement: {replacement}")
    print(f"Exclude directory: {exclude_dirs}")
    print(f"Exclude extensions: {exclude_extensions}")
    
    for root, dirs, files in os.walk(directory):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in files:
            
            file_path = os.path.join(root, filename)
                        
            # Skip binary files and excluded extensions
            if not is_text_file_by_ext(filename) or any(fnmatch.fnmatch(filename, pat) for pat in exclude_extensions):
                continue

            # Skip binary files and excluded extensions
            # if not is_text_file(file_path) or any(fnmatch.fnmatch(filename, pat) for pat in exclude_extensions):
            #     continue
            
            # Read and potentially replace content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Replace content if needle in any format is found
            new_content = content
            for case, variation in needle_variations.items():
                if variation in content:                    
                    new_content = new_content.replace(variation, replacement_variations[case])
                    
                    if dry_run:
                        print(f"Would replace {variation} with {replacement_variations[case]} in {file_path}")
                    else:
                        print(f"Replaced {variation} with {replacement_variations[case]} in {file_path}")

            # If changes were made, write them back to the file or print the action
            if new_content != content and not dry_run:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)

def is_text_file_by_ext(filename: str) -> bool:
    """
    Guess if a file is a text file based on its extension.

    Parameters:
    filename (str): The filename to check.

    Returns:
    bool: True if the file is likely a text file, False otherwise.
    """
    text_file_extensions = [
        '.txt', '.md', '.py', '.js', '.java', '.c', '.cpp', '.cs', '.h', 
        '.html', '.css', '.scss', '.less', '.json', '.xml', '.yaml', '.yml', 
        '.csv', '.log', '.ini', '.conf', '.cfg', '.plist', '.php', '.sh', 
        '.bat', '.cmd', '.ps1', '.vbs', '.rb', '.go', '.lua', '.pl', 
        '.hs', '.lhs', '.scala', '.sbt', '.swift', '.sql', '.r', '.m', 
        '.tex', '.cls', '.sty', '.bib', '.kt', '.groovy', '.gd', '.tcl', 
        '.rst', '.rest', '.http', '.properties', '.toml', '.rs', '.dart', 
        '.xhtml', '.jsp', '.jspx', '.asp', '.aspx', '.erb', '.twig', 
        '.jl', '.ex', '.exs', '.eex', '.leex', '.svelte', '.vue', 
        '.elm', '.cljs', '.clj', '.edn', '.coffee', '.litcoffee', '.iced', 
        '.aj', '.asm', '.s', '.pas', '.p', '.pp', '.f', '.for', '.f90', '.f95', 
        '.ml', '.mli', '.sml', '.thy', '.hs', '.lhs', '.pyw', '.rpy', 
        '.rego', '.rs', '.d', '.rkt', '.sch', '.rktl', '.scm', '.ess', 
        '.rhtml', '.erb', '.mustache', '.hbs', '.phtml', '.twig', '.ctp', 
        '.module', '.inc', '.bash', '.ksh', '.csh', '.fish', '.awk', 
        '.ps', '.nix', '.bb', '.bbappend', '.bbclass', '.recipe', 
        '.lisp', '.lsp', '.l', '.ny', '.pod', '.pm', '.t', '.pl', 
        '.php4', '.php5', '.phtml', '.ctp', '.twig', '.module', 
        '.vb', '.bas', '.cls', '.ctl', '.dsr', '.frm', '.vba', 
        '.applescript', '.osascript', '.ino', '.eps', '.pgn', '.sk', 
        '.brs', '.brightscript', '.sublime-commands', '.sublime-completions', 
        '.sublime-keymap', '.sublime-macro', '.sublime-menu', '.sublime-mousemap', 
        '.sublime-project', '.sublime-settings', '.sublime-snippet', '.sublime-theme', 
        '.sublime-workspace', '.sublime_metrics', '.sublime_session'
        # Add more as needed
    ]
    return any(filename.lower().endswith(ext) for ext in text_file_extensions)

def is_text_file(filepath: str) -> bool:
    """
    Check if a file is a text file based on its MIME type guessed from the extension.

    Parameters:
    filepath (str): The full path to the file to check.

    Returns:
    bool: True if the file is likely a text file, False otherwise.
    """
    # Guess the MIME type of the file based on its extension
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        # Unable to guess the MIME type, not a recognized text file extension
        return False
    return mime_type.startswith('text/')

        
def main():
    import argparse
    
    # Set up the argument parser with optional named arguments
    parser = argparse.ArgumentParser(description='Rename files and replace content within a directory and its subdirectories.')
    parser.add_argument('directory', nargs='?', type=str, help='The directory to rename files in.')
    parser.add_argument('-n', '--needle', type=str, help='The substring to find in filenames for renaming.')
    parser.add_argument('-r', '--replacement', type=str, help='The substring to replace the needle with in filenames.')
    parser.add_argument('-f', '--files', action='store_true', help='The substring to replace the needle with into all text files.')
    parser.add_argument('-d','--dry-run', action='store_true', help='Print out the rename actions without performing them.')
    parser.add_argument('-y','--yes', action='store_true', help='Do not ask for confirmation before performing rename and replace operation.')
    parser.add_argument('--exclude-dirs', nargs='*', help='A list of directories to exclude from renaming.')
    parser.add_argument('--exclude-extensions', nargs='*', help='A list of file extensions to exclude from renaming.')
    
    
    # Parse the arguments
    args, unknown = parser.parse_known_args()
    
    # Handle positional arguments if needle and replacement were not provided as named arguments
    if not args.needle or not args.replacement:
        if len(unknown) == 2:
            args.needle, args.replacement = unknown
        else:
            parser.error("If not using --needle/-n and --replacement/-r, both needle and replacement must be provided as positional arguments.")

    # Check if the directory is provided and valid
    if not args.directory or not os.path.exists(args.directory) or not os.listdir(args.directory):
        raise ValueError(f"The directory is required and must not be empty or non-existent.")

    # Check if needle is provided and valid
    if not args.needle:
        raise ValueError("The needle must be provided and must not be empty or only whitespace.")

    # Ask for confirmation if replacement is empty
    if args.replacement is None:
        confirmation = input("The replacement string is empty. This will remove the needle from filenames. Are you sure you want to continue? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation cancelled.")
            return
    else:
        args.replacement = args.replacement  # Ensure replacement is not None

    # Call the rename_files function
    try:
        rename_files(
            args.directory,
            args.needle,
            args.replacement,
            exclude_dirs=args.exclude_dirs,
            dry_run=args.dry_run,
            ask=not args.yes
        )
        if args.files:
            replace_in_files(
                args.directory,
                args.needle,
                args.replacement,
                exclude_dirs=args.exclude_dirs,
                exclude_extensions=args.exclude_extensions,
                dry_run=args.dry_run,
                 ask=not args.yes
            )
    except ValueError as e:
        print(e)
        exit(1)

if __name__ == '__main__':
    main()  