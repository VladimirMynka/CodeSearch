import ast


class AugAssignVisitor(ast.NodeTransformer):
    def visit_AugAssign(self, node: ast.AugAssign):
        return ast.Assign(
            targets=[node.target],
            value=ast.BinOp(
                left=ast.Name(node.target.id, ast.Load()),
                op=node.op,
                right=node.value
            ),
            lineno=node.lineno
        )
