import ast
import inspect


class MethodCallTransformer(ast.NodeTransformer):
    def __init__(self, context):
        super(MethodCallTransformer, self).__init__()
        self.context = context

    def visit_Assign(self, node: ast.Assign):
        if not isinstance(node.value, ast.Call):
            return node
        new_node = []
        func: ast.Call = node.value
        func_def: ast.FunctionDef = ast.parse(self.context[func.func.id]).body[0]

        assign_left = [ast.Tuple([ast.Name(arg.arg) for arg in func_def.args.args], ast.Store())]
        assign_right = ast.Tuple(func.args, ast.Load())

        new_node.append(ast.Assign(assign_left, assign_right, lineno=node.lineno))
        new_node.extend([i for i in func_def.body if not isinstance(i, ast.Return)])

        returned: ast.Return = [i for i in func_def.body if isinstance(i, ast.Return)][0]
        new_node.append(ast.Assign(node.targets, returned.value, lineno=node.lineno))

        return new_node
