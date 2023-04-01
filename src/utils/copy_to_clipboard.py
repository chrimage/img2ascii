import sys
import os
import argparse
import pyperclip
import re

LANGUAGE_EXTENSIONS_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.c': 'c',
    '.cpp': 'cpp',
    '.java': 'java',
    '.html': 'html',
    '.css': 'css',
    '.go': 'go',
    '.rb': 'ruby',
    '.rs': 'rust',
    '.sh': 'bash',
    '.swift': 'swift',
    '.ts': 'typescript',
    '.php': 'php',
    '.cs': 'csharp',
    '.pl': 'perl',
    '.scala': 'scala',
    '.lua': 'lua',
    '.yaml': 'yaml',
    '.json': 'json',
    '.xml': 'xml',
    # Add more language mappings if needed
}

INTERPRETER_MAP = {
    '.py': 'python3',
    '.sh': 'bash',
    # Add more interpreter mappings if needed
}

class InvalidFilePathError(Exception):
    pass

def read_file_content(filename, encoding=None):
    try:
        with open(filename, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise InvalidFilePathError(f'Error reading {filename}: {str(e)}')

def detect_language(filename):
    extension = os.path.splitext(filename)[1]
    return LANGUAGE_EXTENSIONS_MAP.get(extension, '')

def add_shebang_line_if_missing(file_content, filename):
    extension = os.path.splitext(filename)[1]
    interpreter = INTERPRETER_MAP.get(extension)
    if interpreter:
        shebang_line = file_content.strip().splitlines()[0]
        if not re.match(rf'^#!.*\b{interpreter}\b', shebang_line):
            file_content = f'#!/usr/bin/env {interpreter}\n' + file_content
    return file_content

def copy_to_clipboard(filenames, encoding=None, exclude_empty_files=False, initial_comment=''):
    content = []
    for index, filename in enumerate(filenames):
        if os.path.isfile(filename):
            file_content = read_file_content(filename, encoding).rstrip()
            file_content = add_shebang_line_if_missing(file_content, filename)
            language = detect_language(filename)
            if file_content or not exclude_empty_files:
                if initial_comment:
                    content.append(initial_comment.strip())
                content.append(f'Filename: {filename}')
                content.append(f'```{language}')
                content.append(file_content)
                content.append('```')
                if len(filenames) > 1 and index < len(filenames) - 1:
                    content.append('---')
        else:
            raise InvalidFilePathError(f'{filename} is not a valid file. Please provide a valid file path.')

    if content:
        clipboard_content = '\n'.join(content)
        if encoding:
            clipboard_content = clipboard_content.encode(encoding)
        pyperclip.copy(clipboard_content)
        print('The contents of the following files have been copied to the clipboard:')
        for filename in filenames:
            if os.path.isfile(filename):
                print(f'- {filename}')
    else:
        print('No valid or non-empty files were provided.')

def parse_args():
    parser = argparse.ArgumentParser(description='Copy the contents of one or more files to the clipboard as code blocks.')
    parser.add_argument('files', metavar='file', type=str, nargs='+', help='a file to copy its content to clipboard')
    parser.add_argument('-e', '--encoding', type=str, default=None, help='the encoding to use when reading the files (default: None)')
    parser.add_argument('--exclude-empty-files', action='store_true', help='exclude empty files from clipboard output (default: False)')
    parser.add_argument('-c', '--initial-comment', type=str, default='', help='include an initial comment highlighting context or task (default: empty)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    try:
        copy_to_clipboard(args.files, args.encoding, args.exclude_empty_files, args.initial_comment)
    except InvalidFilePathError as e:
        print(f'Error: {e}')