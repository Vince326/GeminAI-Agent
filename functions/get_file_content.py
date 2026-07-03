import os
from pathlib import Path
from config import MAX_CHARS
from google.genai import types

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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory, with a maximum character limit",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

