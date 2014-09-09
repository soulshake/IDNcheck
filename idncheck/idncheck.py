#!/usr/bin/env python
from __future__ import print_function
import sys
import os.path

# Accepts an identifier (not FQDN) and returns information about the scripts it is composed of
# Usage: ./check.py exampleIDN

aspirational_use_scripts = set(
    ['Canadian_Aboriginal',
    'Miao',
    'Mongolian',
    'Tifinagh',
    'Yi']
    )

recommended_scripts = set(
    ['Common',
    'Inherited',
    'Arabic',
    'Armenian',
    'Bengali',
    'Bopomofo',
    'Cyrillic',
    'Devanagari',
    'Ethiopic',
    'Georgian',
    'Greek',
    'Gujarati',
    'Gurmukhi',
    'Han',
    'Hangul',
    'Hebrew',
    'Hiragana',
    'Kannada',
    'Katakana',
    'Khmer',
    'Lao',
    'Latin',
    'Malayalam',
    'Myanmar',
    'Oriya',
    'Sinhala',
    'Tamil',
    'Telugu',
    'Thaana',
    'Thai',
    'Tibetan',]
)


def file_parse(filename):
    """Parse file containing Unicode code point data"""
    all_scripts = set()

    for line in open(filename):
        if line[0] == '#':
            continue
        if line == '\n':
            continue
        
        words = line.split()
        point_or_range, script_type = words[0], words[2]
        
        # If line includes a range of code points, loop through them
        # E.g.:   003A..003B    ; Common # Po   [2] COLON..SEMICOLON
        if '..' in line:
            hex_range = point_or_range
            range_add(hex_range, script_type)
        else:
            code_point = prefix_0x(point_or_range)
            point_add(code_point, script_type)

def range_add(hex_range, script_type):
    """Add a range of code points"""
    hex_range = hex_range.split('..')
    begin_point, end_point = prefix_0x(hex_range[0]), prefix_0x(hex_range[1])
    for code_point in range(begin_point, end_point + 1):
        point_add(code_point, script_type)

def point_add(code_point, script_type):
    """Add a single code point"""
    scripts_dict[code_point] = script_type

def prefix_0x(code_point):
    return eval ('0x' + code_point)

def char_check(character):
    """Accept a single character and return the script it corresponds to"""
    char_unicode_code_point = ord(character)
    script_type = lookup_script_type(char_unicode_code_point)
    return script_type

def lookup_script_type(code_point):
    return scripts_dict[code_point]

### IDN TESTS ###

def is_ascii(s):
    """Domain name is composed entirely of ASCII"""
    return all(ord(c) < 128 for c in s)

def is_single_script(identifier):
    "Domain name is composed entirely of a single script"""
    return len(get_scripts(identifier)) == 1

def is_highly_restrictive(identifier):
    """Highly restrictive: Domain name is multiple scripts, but from appropriate Japanese combination"""
    scripts_present = get_scripts(identifier)
    if scripts_present <= set(['Latin', 'Han', 'Hiragana', 'Katakana']) \
        or scripts_present <= set(['Hiragana', 'Latin', 'Bopomofo']) \
        or scripts_present <= set(['Hiragana', 'Latin', 'Hangul']):
        return True
    else:
        return False

def is_moderately_restrictive(identifier):
    """Moderately Restrictive: Same as highly restrictive, but allow Latin with other Recommended or Aspirational scripts except Cyrillic and Greek"""
    scripts_present = get_scripts(identifier)
#     if 'Cyrillic' in scripts_present or 'Greek' in scripts_present:
    if scripts_present.intersection(set(['Cyrillic', 'Greek'])):
        return False
    if scripts_present >= recommended_scripts \
        or scripts_present >= aspirational_use_scripts:
        return False
    
    else:
        return True

def is_minimally_restrictive(identifier):
    """Minimally restrictive: Same as moderately restrictive, but allow arbitrary 
    mixtures of scripts"""
    # FIXME dafuq izdat or whatever
    return True

def is_unrestricted(identifier):
    """Unrestricted: Any valid identifiers, including characters outside of 
    the Identifier Profile"""
    return True

def file_download():
    if not os.path.isfile("Scripts.txt"):
        os.system('wget http://www.unicode.org/Public/UNIDATA/Scripts.txt')
    if not os.path.isfile("Scripts.txt"):
        print("There seems to be something broken with the internets :(")
        exit()

def setup():
    file_parse("Scripts.txt")

def get_scripts(identifier):
    # Look up each character in identifier, and append detected scripts to 
    # scripts_present set
    scripts_present = set()
    # FIXME: Consider using set comprehension, maybe later
    for c in identifier:
        scripts_present.add(char_check(c))
    return scripts_present
    
def get_restriction_level(identifier):
    # If input contains multiple identifiers (e.g. example.com), return highest level
    # Iterate through level tests until we pass one by 
    # running the functions listed in the restriction_levels dict
    test_results = {}

    for level, function in restriction_levels:
        test_results[level] = function(identifier)

    for level, function in restriction_levels:
        if test_results[level]:
            levels = level
            break
        else:
            pass

    return levels
    
restriction_levels = [
    (1, is_ascii),
    (2, is_single_script),
    (3, is_highly_restrictive), 
    (4, is_moderately_restrictive),
    (5, is_minimally_restrictive),
    (6, is_unrestricted),
    ]

scripts_dict = {}
file_download()
setup()

# Create a set of all the different scripts we know how to check for
all_scripts = sorted(list(set(scripts_dict.values())))

idncheck = get_restriction_level

if __name__ == "__main__":
    string_to_check = sys.argv[1].decode('utf-8')
    if '.' in string_to_check:
        print("Error: one identifier at a time pls")
        exit()

    if '--all' in string_to_check:
        for s in all_scripts:
            print(s)

    else:
        print(get_restriction_level(string_to_check))
