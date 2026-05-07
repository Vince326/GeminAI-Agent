import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(full_path)

        if os.path.commonpath([abs_working, abs_target]) != abs_working:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_target]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, cwd=abs_working, text=True, timeout=30)
        pieces = []
        if result.returncode!= 0:
             pieces.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            pieces.append("No output produced")
        else:
            if result.stdout:
                    pieces.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                    pieces.append(f"STDERR: {result.stderr}")
        return "\n".join(pieces)
    except Exception as e:
        return f"Error: executing Python file: {e}"