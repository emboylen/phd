"""Rebuild refined-topic-model.py with correct indentation and processes=1 fix"""

# We'll rebuild the file from the parts we know work
# Everything before line 215 was correct
# We just need to remove the bad if __name__ block and fix the CoherenceModel line

with open("refined-topic-model.py.backup", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find where the bad section starts (if __name__ line)
bad_start = None
for i, line in enumerate(lines):
    if "if __name__ == '__main__':" in line and i > 200:
        bad_start = i
        break

if bad_start:
    print(f"Found bad if __name__ at line {bad_start + 1}")
    
    # Write everything up to the bad section
    with open("refined-topic-model.py", "w", encoding="utf-8") as f:
        # Write lines before the if __name__
        for i in range(bad_start):
            f.write(lines[i])
        
        # Skip the if __name__ block and find where real code resumes
        # Look for "# Validate PDF folder" or similar
        i = bad_start
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "freeze_support" not in line and "if __name__" not in line:
                # Found first real code line
                # Now write from here, removing any excess indentation
                print(f"Found real code resuming at line {i + 1}")
                for j in range(i, len(lines)):
                    original_line = lines[j]
                    stripped = original_line.lstrip()
                    if not stripped:
                        f.write("\n")
                    else:
                        # Calculate original indent and preserve relative structure
                        orig_spaces = len(original_line) - len(stripped)
                        # If it had 4+ spaces, reduce by 4
                        if orig_spaces >= 4:
                            new_indent = " " * (orig_spaces - 4)
                            f.write(new_indent + stripped)
                        else:
                            f.write(stripped)
                break
            i += 1
    
    print("File rebuilt!")
else:
    print("Could not find if __name__ block")
