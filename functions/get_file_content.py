import os
from pathlib import Path
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_directory, target_dir]) != working_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_dir, 'r') as file:
            contents = file.read(MAX_CHARS)
            if file.read(1):
                contents += f"{file_path} content truncated at {MAX_CHARS} characters."
    except Exception as e:
        return f'Error: Failed to read file "{file_path}": {str(e)}'
    return contents

