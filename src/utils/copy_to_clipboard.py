#!/usr/bin/env python3
import sys
import os
import argparse
import pyperclip
import re
import glob

LANGUAGE_EXTENSIONS_MAP = {
    '.py': 'python',
    '.txt': 'plaintext',
    '.md': 'markdown',
}

EXTENSIONS_SUPPORTED = ["*.py", "*.txt", "*.md"]

class InvalidFilePathError(Exception):
    pass

def strip_comments_and_docstrings(content, file_ext, strip_comments, strip_docstrings):
    if file_ext == '.py':
        if strip_comments:
            content = re.sub(r"(?m)(^#.*$)", "", content)

        if strip_docstrings:
            content = re.sub(r"(?ms)('''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")", "", content)
    return content

def read_file_content(filename, encoding=None, strip_comments=False, strip_docstrings=False):
    try:
        with open(filename, 'r', encoding=encoding) as f:
            content = f.read()
            file_ext = os.path.splitext(filename)[1]
            content = strip_comments_and_docstrings(content, file_ext, strip_comments, strip_docstrings)
            return content
    except Exception as e:
        raise InvalidFilePathError(f'Error reading {filename}: {str(e)}')

def get_files_recursive(paths, extensions_supported=None):
    files = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    if not extensions_supported or any(filename.endswith(ext[1:]) for ext in extensions_supported):
                        files.append(os.path.join(root, filename))
        elif os.path.isfile(path):
            if not extensions_supported or any(path.endswith(ext[1:]) for ext in extensions_supported):
                files.append(path)
        else:
            for ext in extensions_supported or []:
                for filepath in glob.glob(os.path.join(path, ext)):
                    files.append(filepath)

        if not files and os.path.isdir(path):
            for ext in extensions_supported or []:
                for filepath in glob.glob(os.path.join(path, ext)):
                    files.append(filepath)

    return files

def parse_args():
    parser = argparse.ArgumentParser(description='Copy the contents of one or more files to the clipboard as code blocks.')
    parser.add_argument('input', metavar='input', type=str, nargs='*', help='a file or a directory to copy its content to clipboard')
    parser.add_argument('-e', '--encoding', type=str, default=None, help='the encoding to use when reading the files (default: None)')
    parser.add_argument('--strip-comments', action='store_true', help='remove comments from the code (default: False)')
    parser.add_argument('--strip-docstrings', action='store_true', help='remove docstrings from the code (default: False)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    try:
        files = get_files_recursive(args.input, EXTENSIONS_SUPPORTED)
        if files:
            content = []
            for index, filename in enumerate(files):
                file_content = read_file_content(filename, args.encoding, args.strip_comments, args.strip_docstrings).rstrip()
                
                if not file_content:
                    continue
                
                language = LANGUAGE_EXTENSIONS_MAP.get(os.path.splitext(filename)[1], '')
                content.append(f'Filename: {filename}')
                content.append(f'```{language}')
                content.append(file_content)
                content.append('```')

                if index < len(files) - 1:
                    content.append('---')
    
            clipboard_content = '\n'.join(content)
            pyperclip.copy(clipboard_content)
            print('The contents of the following files have been copied to the clipboard:')
            for filename in files:
                print(f'- {filename}')
        else:
            print('No valid or non-empty files were provided.')

    except InvalidFilePathError as e:
        print(f'Error: {e}')