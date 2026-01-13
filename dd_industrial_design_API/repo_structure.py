import os

def print_directory_structure(root_dir, max_depth=2, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'venv', '__pycache__', 'node_modules', 'env', 'build', 'dist'}

    for root, dirs, files in os.walk(root_dir):
        # Calculate the current depth based on the root relative to root_dir
        level = root.replace(root_dir, '').count(os.sep)
        
        # Skip deeper directories than max_depth
        if level > max_depth:
            continue

        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")

        # Exclude unwanted directories from further walking
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # List files at this level only if we are not deeper than max_depth
        if level < max_depth:
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")

if __name__ == "__main__":
    # Use '.' as the root_dir if you run the script from your project's root
    print_directory_structure('.', max_depth=2)
