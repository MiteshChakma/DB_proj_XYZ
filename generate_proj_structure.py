import os

def generate_project_structure(root_dir=None, file_name="project_structure.md"):
    if root_dir is None:
        root_dir = os.getcwd()  # Get current working directory

    try:
        with open(file_name, 'w') as file:
            for root, dirs, files in os.walk(root_dir, topdown=True):
                level = root.replace(root_dir, '').count(os.sep)
                indent = ' ' * 4 * (level)
                file.write('{}{}/\n'.format(indent, os.path.basename(root)))
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    file.write('{}{}\n'.format(subindent, f))
        print("Project structure written to", file_name)
    except Exception as e:
        print("Error:", e)

generate_project_structure()
