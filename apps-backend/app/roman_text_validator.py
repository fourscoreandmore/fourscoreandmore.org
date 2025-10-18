"""
Roman Text Validator

This module provides validation utilities for Roman text analysis files
to ensure compatibility with music21 9.x and provide better error messages.

music21 9.x has stricter parsing requirements and will crash with an
AttributeError ('NoneType' object has no attribute 'quarterLength') when
parsing Roman text files that have no Roman numerals (e.g., empty templates).
"""


def validate_roman_text_file(filepath):
    """
    Validates a Roman text file to ensure it has at least one Roman numeral.
    
    This prevents cryptic errors from music21 9.x when parsing empty or 
    template files that contain only metadata and measure markers without
    any actual Roman numeral annotations.
    
    Args:
        filepath: Path to the Roman text file to validate
        
    Raises:
        ValueError: If the file contains no Roman numerals
        
    Returns:
        True if validation passes
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    has_roman_numeral = False
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, comments, and metadata
        if not line or line.startswith('Composer:') or line.startswith('Title:') or \
           line.startswith('Analyst:') or line.startswith('Proofreader:') or \
           line.startswith('Note:') or line.startswith('Time Signature:'):
            continue
            
        # Check if line contains a measure marker
        if line.startswith('m'):
            # Check if it has any content after the beat marker
            parts = line.split()
            if len(parts) > 2:  # Has measure, beat, and at least one Roman numeral
                has_roman_numeral = True
                break
    
    if not has_roman_numeral:
        msg = ('The Roman text file appears to be empty or contains no Roman numerals. '
               'This is likely a template file that needs to be filled in. '
               'Please add at least one Roman numeral (e.g., "m1 b1 C: I") before analyzing.')
        raise ValueError(msg)
    
    return True
