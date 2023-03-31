import ast


class VariableTransformer(ast.NodeTransformer):
    expr_num = 0

    def __init__(self, var_list):
        super().__init__()
        self.var_list = var_list

    def visit_arg(self, node: ast.arg):
        node.arg = self.var_list[self.expr_num]
        self.expr_num += 1
        return node

    def visit_Name(self, node: ast.Name):
        node.id = self.var_list[self.expr_num]
        self.expr_num += 1
        return node
