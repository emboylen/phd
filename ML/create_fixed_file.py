"""Create a properly fixed version of refined-topic-model.py"""

with open('refined-topic-model.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Read {len(lines)} lines from original file")

# Everything up to line 210 is correct (imports, configs, functions)
# We need to add proper if __name__ guard and indent everything after

with open('refined-topic-model.py', 'w', encoding='utf-8') as f:
    # Write lines 1-210 as-is (these are correct - imports, config, functions)
    for i in range(210):
        f.write(lines[i])
    
    # Add the if __name__ guard
    f.write('\n')
    f.write('# ==============================================================================\n')
    f.write('# MAIN EXECUTION\n')
    f.write('# ==============================================================================\n')
    f.write("if __name__ == '__main__':\n")
    f.write('    # Required for Windows multiprocessing support\n')
    f.write('    from multiprocessing import freeze_support\n')
    f.write('    freeze_support()\n')
    f.write('\n')
    
    # Now process lines starting from 220 onwards
    # We need to normalize the indentation - everything should be indented 4 spaces from base
    # Current file has mixed indentation (4, 8, 12 spaces)
    
    for i in range(220, len(lines)):
        line = lines[i]
        stripped = line.lstrip()
        
        if not stripped:  # Empty line
            f.write('\n')
            continue
            
        # Calculate original indentation level
        orig_indent = len(line) - len(stripped)
        indent_level = orig_indent // 4
        
        # Add base 4-space indent for if __name__, then add relative indentation  
        new_line = '    ' + ('    ' * indent_level) + stripped
        f.write(new_line)

print("File fixed successfully!")
print("Created: refined-topic-model.py with proper Windows multiprocessing support")

