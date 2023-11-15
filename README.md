# File Renamer and Replacer Script

This Python script is designed to rename files and replace text within files across a directory and its subdirectories.

## Features

- **Case-Sensitive Renaming and Replacing:** The script not only renames files but also searches through the content of text files. It identifies the case format (camelCase, PascalCase, snake_case, kebab-case) of the needle (the text to be replaced) and applies the replacement text in the same case format. This ensures that the replacement is consistent with the original text's styling and naming conventions, which is particularly important in codebases where variable and function names may have specific case requirements.

- **Flexible Exclusions:** You can specify directories to exclude from the renaming process to keep certain parts of your project untouched. Additionally, you can exclude specific file extensions if you want to limit the scope of the script to certain file types.

- **Dry Run Option:** Before making any permanent changes, you can perform a dry run to preview the changes. This feature prints out all the actions that would be taken, allowing you to verify the script's operations before it modifies any files.

- **Recursion Through Subdirectories:** The script operates recursively through all subdirectories of the provided path, ensuring comprehensive renaming and replacing throughout the entire directory tree.

## Usage

Run the script from the command line using the following format:

```bash
python rename_script.py "/path/to/directory" "oldText" "newText" --dry-run
```

Add `-f` or `--files` to remplace texte inside file to

```bash
python rename_script.py "/path/to/directory" "oldText" "newText" --dry-run -f
```

To use with optional arguments for needle and replacement:

```bash
python rename_script.py "/path/to/directory" -n "oldText" -r "newText" --dry-run
```

To use with optional arguments for needle and replacement:

```bash
python rename_script.py "/path/to/directory" -n "oldText" -r "newText" --dry-run
```
