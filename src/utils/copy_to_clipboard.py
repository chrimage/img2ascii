#!/usr/bin/env python3

import sys
import os
import pyperclip

def copy_to_clipboard(filenames):
    content = []
    for filename in filenames:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                content.append(f'Filename: {filename}')
                content.append('```')
                content.extend(line.rstrip() for line in f if line.strip())
                content.append('```')

    if content:
        clipboard_content = '\n'.join(content)
        pyperclip.copy(clipboard_content)
        print('The contents of the following files have been copied to the clipboard:')
        for filename in filenames:
            print(f'- {filename}')
    else:
        print('No valid files were provided.')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: copy_to_clipboard.py [file1] [file2] ...')
    else:
        filenames = sys.argv[1:]
        copy_to_clipboard(filenames)
