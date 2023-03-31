import ast


class VariableCounter(ast.NodeVisitor):
    name_map = {}
    expr_num = 0

    def visit_arg(self, node: ast.arg):
        self.name_map[node.arg] = {
            'defines': [(-1, self.expr_num)],
            'usages': []
        }
        self.expr_num += 1

    def visit_Name(self, node: ast.Name):
        if node.id not in self.name_map:
            self.name_map[node.id] = {
                'defines': [],
                'usages': []
            }
        us_or_def = 'usages' if isinstance(node.ctx, ast.Load) else 'defines'
        self.name_map[node.id][us_or_def].append((node.lineno, self.expr_num))
        self.expr_num += 1
