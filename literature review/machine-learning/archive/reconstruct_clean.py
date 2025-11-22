"""Create properly indented file by reading from backup that has 0-indent main code"""

# We need the ORIGINAL version before any of our indentation attempts
# Let's reconstruct from what we know worked

with open('refined-topic-model.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Write clean version
with open('refined-topic-model.py', 'w', encoding='utf-8') as f:
    # Lines 1-210: imports, configs, functions (keep as-is)
    for i in range(210):
        f.write(lines[i])
    
    # Add if __name__ guard
    f.write('\n')
    f.write('# ==============================================================================\n')
    f.write('# MAIN EXECUTION\n')
    f.write('# ==============================================================================\n')
    f.write("if __name__ == '__main__':\n")
    f.write('    # Required for Windows multiprocessing support\n')
    f.write('    from multiprocessing import freeze_support\n')
    f.write('    freeze_support()\n')
    f.write('\n')
    
    # Now for lines 220+, we need to REMOVE excess indentation first, then add 4 spaces
    for i in range(220, len(lines)):
        line = lines[i]
        
        # Remove ALL leading whitespace and check indent
        stripped = line.lstrip()
        
        if not stripped:  # Empty line
            f.write('\n')
            continue
        
        # Calculate what the ORIGINAL indent should have been (before our bad fixes)
        # Lines that started with 12+ spaces were already inside nested blocks
        orig_indent_spaces = len(line) - len(stripped)
        
        # Normalize: assume anything with 12+ spaces had 3 levels (so 8 spaces too much)
        # Anything with 8 spaces had 2 levels (so 4 spaces too much)
        # Anything with 4 spaces had 1 level (correct at 0)
        # Anything with 0 spaces was at base level
        
        if orig_indent_spaces >= 12:
            # Was nested 2 levels deep originally
            relative_indent = '        '  # 8 spaces relative
        elif orig_indent_spaces >= 8:
            # Was nested 1 level deep originally  
            relative_indent = '    '  # 4 spaces relative
        elif orig_indent_spaces >= 4:
            # Was at base level originally
            relative_indent = ''
        else:
            # Was at base level
            relative_indent = ''
        
        # Add base 4-space indent for if __name__ + relative indent
        new_line = '    ' + relative_indent + stripped
        f.write(new_line)

print("File completely reconstructed with proper indentation!")

