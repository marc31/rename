import unittest

import sys
import os
import tempfile
from shutil import copytree, rmtree

# Add the parent directory to sys.path to import the module located there
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rename import to_pascal_case, to_camel_case, to_snake_case, to_kebab_case, detect_case_type, convert_string, generate_all_case_variations,replace_text_in_filename, rename_files, replace_in_files

class TestNamingConversions(unittest.TestCase):

    def setUp(self):
        # Set up the case variations for the needle and the replacement
        self.needle = 'example'
        self.replacement = 'sample'
        self.needle_variations = generate_all_case_variations(self.needle)
        self.replacement_variations = generate_all_case_variations(self.replacement)
        
        # Set up a temporary directory
        self.temp_dir = tempfile.mkdtemp()

        # Create subdirectories and files for testing
        os.makedirs(os.path.join(self.temp_dir, 'rename_file_test_dir'), exist_ok=True)
        with open(os.path.join(self.temp_dir, 'example_test_file.txt'), 'w') as f:
            f.write('This is a test file.')
        with open(os.path.join(self.temp_dir, 'rename_file_test_dir', 'example_test_file2.txt'), 'w') as f:
            f.write('This is another test file.')
                        
    def tearDown(self):
        # Remove the temporary directory after the test
        rmtree(self.temp_dir)
        
    # Test cases for to_pascal_case function
    def test_to_pascal_case(self):
        self.assertEqual(to_pascal_case('this-is-kebab-case'), 'ThisIsKebabCase')
        self.assertEqual(to_pascal_case('this-is-1-keb1ab-case-string'), 'ThisIs1Keb1abCaseString')
  
    # Test cases for to_camel_case function
    def test_to_camel_case(self):
        self.assertEqual(to_camel_case('this-is-kebab-case'), 'thisIsKebabCase')
        self.assertEqual(to_camel_case('this-is-1-keb1ab-case-string'), 'thisIs1Keb1abCaseString')
     
    # Test cases for to_snake_case function
    def test_to_snake_case(self):
        self.assertEqual(to_snake_case('this-is-kebab-case'), 'this_is_kebab_case')
        self.assertEqual(to_snake_case('this-is-1-keb1ab-case-string'), 'this_is_1_keb1ab_case_string')

    # Test cases for to_kebab_case function
    def test_to_kebab_case(self):
        self.assertEqual(to_kebab_case('ThisIsCamelCase'), 'this-is-camel-case')
        self.assertEqual(to_kebab_case('ThisIsPascalCase'), 'this-is-pascal-case')
        self.assertEqual(to_kebab_case('this_is_snake_case'), 'this-is-snake-case')
        self.assertEqual(to_kebab_case('this-is-already-kebab-case'), 'this-is-already-kebab-case')
        self.assertEqual(to_kebab_case('This-Is_Already_Mixed'), 'this-is-already-mixed')
        self.assertEqual(to_kebab_case('This--Is_Already_Mixed'), 'this-is-already-mixed')
        self.assertEqual(to_kebab_case('This-1-Is_Alre1ady_Mixed'), 'this-1-is-alre1ady-mixed')
        
    # Test cases for detect_case_type function
    def test_detect_case_type(self):
        
        self.assertEqual(detect_case_type('camelCaseString'), 'camelCase')
        self.assertEqual(detect_case_type('came1l1CaseString'), 'camelCase')
        self.assertEqual(detect_case_type('thisIsAlreadyCamelCase'), 'camelCase')
        self.assertEqual(detect_case_type('isJSON'), 'camelCase')
                
        self.assertEqual(detect_case_type('PascalCaseString'), 'PascalCase')
        self.assertEqual(detect_case_type('Pasca1lCa1seString'), 'PascalCase')
        self.assertEqual(detect_case_type('NoConvention123'), 'PascalCase')
        self.assertEqual(detect_case_type('XMLHttpRequest'), 'PascalCase')
        
        self.assertEqual(detect_case_type('snake_case_string'), 'snake_case')
        self.assertEqual(detect_case_type('snak1e1_1case_string'), 'snake_case')
                
        self.assertEqual(detect_case_type('kebab-case-string'), 'kebab-case')
        self.assertEqual(detect_case_type('keba1b1-1case-string'), 'kebab-case')

    def test_convert_to_camel_case(self):
        self.assertEqual(convert_string('this-is-kebab-case', 'camelCase'), 'thisIsKebabCase')
        self.assertEqual(convert_string('this_is_snake_case', 'camelCase'), 'thisIsSnakeCase')
        self.assertEqual(convert_string('ThisIsPascalCase', 'camelCase'), 'thisIsPascalCase')
        self.assertEqual(convert_string('thisIsCamelCase', 'camelCase'), 'thisIsCamelCase')

    def test_convert_to_pascal_case(self):
        self.assertEqual(convert_string('this-is-kebab-case', 'PascalCase'), 'ThisIsKebabCase')
        self.assertEqual(convert_string('this_is_snake_case', 'PascalCase'), 'ThisIsSnakeCase')
        self.assertEqual(convert_string('ThisIsPascalCase', 'PascalCase'), 'ThisIsPascalCase')
        self.assertEqual(convert_string('thisIsCamelCase', 'PascalCase'), 'ThisIsCamelCase')

    def test_convert_to_snake_case(self):
        self.assertEqual(convert_string('this-is-kebab-case', 'snake_case'), 'this_is_kebab_case')
        self.assertEqual(convert_string('this_is_snake_case', 'snake_case'), 'this_is_snake_case')
        self.assertEqual(convert_string('ThisIsPascalCase', 'snake_case'), 'this_is_pascal_case')
        self.assertEqual(convert_string('thisIsCamelCase', 'snake_case'), 'this_is_camel_case')

    def test_convert_to_kebab_case(self):
        self.assertEqual(convert_string('this-is-kebab-case', 'kebab-case'), 'this-is-kebab-case')
        self.assertEqual(convert_string('this_is_snake_case', 'kebab-case'), 'this-is-snake-case')
        self.assertEqual(convert_string('ThisIsPascalCase', 'kebab-case'), 'this-is-pascal-case')
        self.assertEqual(convert_string('thisIsCamelCase', 'kebab-case'), 'this-is-camel-case')

    def test_no_conversion(self):
        self.assertEqual(convert_string('AlreadyOtherFormat123', 'other'), 'AlreadyOtherFormat123')

    def test_unsupported_case(self):
        with self.assertRaises(ValueError):
            convert_string('someString', 'unsupportedCase')
        
    def test_convert_naming_conventions(self):
        self.assertEqual(generate_all_case_variations('this-is-kebab-case'), 
        {
            'original': 'this-is-kebab-case',
            'camelCase': 'thisIsKebabCase',
            'PascalCase': 'ThisIsKebabCase',
            'snake_case':  'this_is_kebab_case',
            'kebab-case': 'this-is-kebab-case'
        })
            


    def test_replace_kebab_case(self):
        filename = 'this-is-an-example-file.txt'
        expected = 'this-is-an-sample-file.txt'
        result = replace_text_in_filename(filename, self.needle_variations, self.replacement_variations)
        self.assertEqual(result, expected)

    def test_replace_snake_case(self):
        filename = 'this_is_an_example_file.txt'
        expected = 'this_is_an_sample_file.txt'
        result = replace_text_in_filename(filename, self.needle_variations, self.replacement_variations)
        self.assertEqual(result, expected)

    def test_replace_camel_case(self):
        filename = 'thisIsAnExampleFile.txt'
        expected = 'thisIsAnSampleFile.txt'
        result = replace_text_in_filename(filename, self.needle_variations, self.replacement_variations)
        self.assertEqual(result, expected)

    def test_replace_pascal_case(self):
        filename = 'ThisIsAnExampleFile.txt'
        expected = 'ThisIsAnSampleFile.txt'
        result = replace_text_in_filename(filename, self.needle_variations, self.replacement_variations)
        self.assertEqual(result, expected)

    def test_no_replacement_needed(self):
        filename = 'this-file-does-not-need-change.txt'
        expected = 'this-file-does-not-need-change.txt'
        result = replace_text_in_filename(filename, self.needle_variations, self.replacement_variations)
        self.assertEqual(result, expected)

    def test_replace_with_numbers(self):
        filename = 'example123-file.txt'
        expected = 'sample123-file.txt'
        result = replace_text_in_filename(filename, self.needle_variations, self.replacement_variations)
        self.assertEqual(result, expected)

    def test_replace_multiple_occurrences(self):
        filename = 'example-example-file.txt'
        expected = 'sample-sample-file.txt'
        result = replace_text_in_filename(filename, self.needle_variations, self.replacement_variations)
        self.assertEqual(result, expected)
        
    def test_replace_in_files(self):
        # Test cases in the format: {filename: (original_content, expected_content)}
        test_cases = {
            'test_snake_case.txt': ('this_is_a_test_string', 'this_is_a_demo_example'),
            'TestPascalCase.txt': ('ThisIsATestString', 'ThisIsADemoExample'),
            'testCamelCase.txt': ('thisIsATestString', 'thisIsADemoExample'),
            'test-kebab-case.txt': ('this-is-a-test-string', 'this-is-a-demo-example'),
            'original.txt': ('testString', 'demoExample'),
            # 'lowercase.txt': ('teststring', 'demoexample'),
            # 'UPPERCASE.txt': ('TESTSTRING', 'DEMOEXAMPLE'),
        }
        
        # Print a TODO message
        print("TODO: 'lowercase.txt': ('teststring', 'demoexample'),")
        print("TODO: 'UPPERCASE.txt': ('TESTSTRING', 'DEMOEXAMPLE'),")
        
        # Define the needle and the replacement
        needle = 'testString'
        replacement = 'demoExample'

        os.makedirs(os.path.join(self.temp_dir, 'replace_file_test_dir'), exist_ok=True)
        
        # Create test files and write original content to them
        for filename, (original_content, _) in test_cases.items():
            with open(os.path.join(self.temp_dir, 'replace_file_test_dir', filename), 'w') as f:
                f.write(original_content)

        # Run the replace_in_files function
        replace_in_files(
            self.temp_dir,
            needle,
            replacement,
            exclude_dirs=None,
            exclude_extensions=None,
            dry_run=False,
            ask=False
        )
        
        # Check that the content has been replaced correctly in each file
        for filename, (_, expected_content) in test_cases.items():
            with open(os.path.join(self.temp_dir, 'replace_file_test_dir', filename), 'r') as f:
                content = f.read()
                self.assertEqual(content, expected_content)
       
    def test_rename_files(self):
        # Define the needle and the replacement
        needle = 'example'
        replacement = 'sample'

        # Run the rename_files function
        rename_files(self.temp_dir, needle, replacement, exclude_dirs=None, dry_run=False, ask=False)

        # Check that the files have been renamed
        self.assertTrue(os.path.isfile(os.path.join(self.temp_dir, 'sample_test_file.txt')))
        self.assertTrue(os.path.isfile(os.path.join(self.temp_dir, 'rename_file_test_dir', 'sample_test_file2.txt')))

        # Optionally, you can check the contents of the file to ensure it hasn't been altered
        with open(os.path.join(self.temp_dir, 'sample_test_file.txt'), 'r') as f:
            content = f.read()
            self.assertIn('This is a test file.', content)                       

if __name__ == '__main__':
    unittest.main()
