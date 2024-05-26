import os
import sys


def get_python_executable():
    """Returns the path to the Python executable. Virtual environment-aware."""
    if (virtual_env_path := os.getenv("VIRTUAL_ENV")) is not None:
        return (
            os.path.join(virtual_env_path, "Scripts", "python.exe")
            if os.name == "nt"
            else os.path.join(virtual_env_path, "bin", "python")
        )

    return sys.executable
