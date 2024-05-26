import importlib.util
import sys


def import_module_from_path(module_name: str, module_path: str):
    """Imports Python module file from path.

    Args:
    - module_name (str): Name of the module.
    - module_path (str): Path to the module file.

    Returns:
    - ModuleType: The imported module.
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def import_module_from_path_suppress(module_name: str, module_path: str):
    """The same as `import_module_from_path`, but suppresses any errors.

    Args:
    - module_name (str): Name of the module.
    - module_path (str): Path to the module file.

    Returns:
    - ModuleType: The imported module.
    """
    try:
        return import_module_from_path(module_name, module_path)
    except FileNotFoundError:
        print(f"Error: The file {module_path} does not exist.")
    except SyntaxError as e:
        print(f"Error: Syntax error in the module {module_path}: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
