"""Final complete fix - read lines 1-218, then add proper if __name__ and indent rest with 4 spaces"""

with open('refined-topic-model.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Write corrected file
with open('refined-topic-model.py', 'w', encoding='utf-8') as f:
    # Write lines 1-210 (imports, config, functions) - these are perfect
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
    
    # Read from the FIRST backup we made that should still exist
    try:
        with open('refined-topic-model.py.backup', 'r', encoding='utf-8') as backup:
            backup_lines = backup.readlines()
        
        # From backup, find line with "# Validate PDF folder" - that's where clean code starts
        start_idx = None
        for i, line in enumerate(backup_lines):
            if '# Validate PDF folder' in line or 'pdf_folder = Path(PDF_FOLDER_PATH)' in line:
                # Go back a few lines to get the section header
                for j in range(i-1, max(0, i-10), -1):
                    if 'DATA LOADING' in backup_lines[j]:
                        start_idx = j - 2  # Include the ====== line
                        break
                break
        
        if start_idx and start_idx < len(backup_lines):
            print(f"Found clean code starting at backup line {start_idx}")
            # Copy from backup, adding 4-space indent
            for i in range(start_idx, len(backup_lines)):
                line = backup_lines[i]
                stripped = line.lstrip()
                if not stripped:
                    f.write('\n')
                else:
                    # Get original indent
                    orig_indent = len(line) - len(stripped)
                    # Add 4-space base + original relative indent
                    new_line = '    ' + ' ' * orig_indent + stripped
                    f.write(new_line)
            print("Successfully used backup to restore clean code!")
            exit(0)
    except FileNotFoundError:
        print("No backup found, will try to clean current file...")
    
    # If backup doesn't work, manually clean from current file starting after our last good edit
    # Skip corrupted lines 246+ and reconstruct from line 219 in current file
    print("Reconstructing from current file with manual indent fixes...")
    
    # Just copy lines 220+ from current file, fixing indent as we go
    for i in range(220, len(lines)):
        line = lines[i]
        stripped = line.lstrip()
        
        if not stripped:
            f.write('\n')
            continue
        
        # Remove ALL indent, calculate what it should be based on content
        orig_spaces = len(line) - len(stripped)
        
        # Heuristic: if line has lots of leading spaces, it was nested
        # Try to normalize based on Python syntax
        if stripped.startswith(('if ', 'for ', 'while ', 'try:', 'except', 'with ', 'def ', 'class ')):
            # Block starter - should be at current level
            relative = ''
        elif any(stripped.startswith(kw) for kw in ['return', 'break', 'continue', 'pass', 'raise', 'print', 'logger']):
            # Statement - might be nested
            if orig_spaces >= 12:
                relative = '        '  # 2 levels deep
            elif orig_spaces >= 8:
                relative = '    '  # 1 level deep
            else:
                relative = ''
        elif stripped.startswith('#'):
            # Comment - use original relative indent
            if orig_spaces >= 12:
                relative = '    '
            else:
                relative = ''
        else:
            # Regular code - maintain relative indent
            if orig_spaces >= 12:
                relative = '        '
            elif orig_spaces >= 8:
                relative = '    '
            else:
                relative = ''
        
        new_line = '    ' + relative + stripped
        f.write(new_line)

print("File reconstructed!")

