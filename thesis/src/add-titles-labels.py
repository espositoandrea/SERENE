#!/usr/bin/python3
 
from glob import glob
import re
import unidecode
from colorama import Fore, Style

def replace_function(match):
    title = re.sub(r'[\'\`:]', '', re.sub(r'\s', '-', match.group(3).lower(), 0, re.MULTILINE), 0, re.MULTILINE)
    s = f'{match.group(1)}{{{match.group(3)}}}\\label{{{match.group(2)}:{unidecode.unidecode(title)}}}'
    return s

def set_labels(text):
    text = re.sub(r'^(\\(.*?)(?:(?:ter)|(?:tion)|(?:agraph))\*?)\{(.*?)\}(\\label\{.*?\})?$',
                  lambda match: replace_function(match),
                  text, 0, re.MULTILINE)

    text = re.sub(r'^(\\(part)\*?)\{(.*?)\}(\\label\{.*?\})?$',
                  lambda match: replace_function(match),
                  text, 0, re.MULTILINE)
    return text

if __name__ == "__main__":
    file_paths = glob("chapters/*.tex")
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf8') as f:
            data = f.read()
        data = set_labels(data)
        with open(file_path, 'w', encoding='utf8') as f:
            f.write(data)
        print(f'{Fore.GREEN}File {file_path}: DONE{Style.RESET_ALL}')
