import ast
import inspect


def print_ast(method):
    print(ast.dump(ast.parse(inspect.getsource(method)), indent=4, include_attributes=True))


def get_ast(method):
    return ast.parse(inspect.getsource(method))


def get_ctx(locals_dict):
    return {
        name: inspect.getsource(obj) for (name, obj) in locals_dict
        if hasattr(obj, "__class__") and obj.__class__.__name__ == "function"
    }
