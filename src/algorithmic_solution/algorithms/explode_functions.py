import ast

from src.algorithmic_solution.node_visitors import MethodCallTransformer


def pipeline(code_string: str, ctx: dict):
    mct = MethodCallTransformer(ctx)
    tree = ast.parse(code_string)
    tree = mct.visit(tree)
    tree = ast.fix_missing_locations(tree)

    return ast.unparse(tree)
