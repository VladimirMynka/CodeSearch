import ast

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.algorithmic_solution.node_visitors import VariableTransformer, VariableCounter, AugAssignVisitor


def reform_name_map(name_map):
    new_name_map = {}
    for name in name_map:
        defines = name_map[name]['defines']
        usages = name_map[name]['usages']

        for define, i in zip(defines, range(len(defines))):
            new_name_map[f"{name}___definition___{i}"] = {'define': define, 'usages': []}

        for usage in usages:
            for i in range(len(defines)):
                if (i == len(defines) - 1) or ((defines[i][0] < usage[0]) and (defines[i + 1][0] >= usage[0])):
                    new_name_map[f"{name}___definition___{i}"]['usages'].append(usage)
                    break
    return new_name_map


def name_map_to_pd(name_map):
    res = []
    for name in name_map:
        res.append({
            'name': name,
            'define': name_map[name]['define'],
            'last_usage': None if len(name_map[name]['usages']) == 0 else name_map[name]['usages'][-1],
            'usages': name_map[name]['usages']
        })
    return pd.DataFrame(res)


def calculate_next_steps(pd_name_map):
    sorted_by_usage = pd_name_map.sort_values("last_usage").reset_index(drop=True)
    sorted_by_define = pd_name_map.sort_values("define").reset_index(drop=True)

    next_steps = []
    for i in range(len(sorted_by_usage)):
        for j in range(i + 1, len(sorted_by_define)):
            if j in next_steps:
                continue
            if sorted_by_usage.iloc[i].last_usage[0] <= sorted_by_define.iloc[j].define[0]:
                next_steps.append(j)
                break
        if len(next_steps) != i + 1:
            next_steps.append(None)

    return sorted_by_usage, next_steps


def apply_next_steps(sorted_by_usage, next_steps):
    for next_, i in zip(next_steps, range(len(next_steps))):
        if next_ is None:
            continue
        sorted_by_usage.iloc[next_, 0] = sorted_by_usage.iloc[i, 0]
    return sorted_by_usage


def anonymize_vars(sorted_by_usage):
    le = LabelEncoder()
    sorted_by_usage.name = [f"var_{i}" for i in le.fit_transform(sorted_by_usage.name)]
    return sorted_by_usage


def get_var_list(sorted_by_usage, expr_num):
    sorted_by_usage.define = sorted_by_usage.define.apply(lambda elem: elem[1])
    sorted_by_usage.usages = sorted_by_usage.usages.apply(lambda elem: [j[1] for j in elem])

    sorted_by_usage.usages = sorted_by_usage.apply(lambda row_: row_.usages + [row_.define], axis=1)

    var_list = [''] * expr_num
    for row in sorted_by_usage.iloc:
        for i in row.usages:
            var_list[i] = row["name"]

    return var_list


def clear_variables(ast_tree):
    aav = AugAssignVisitor()
    ast_tree = ast.fix_missing_locations(aav.visit(ast_tree))

    vc = VariableCounter()
    vc.visit(ast_tree)

    name_map = reform_name_map(vc.name_map)

    res = name_map_to_pd(name_map)
    sorted_by_usage, next_steps = calculate_next_steps(res)
    sorted_by_usage = apply_next_steps(sorted_by_usage, next_steps)
    sorted_by_usage = anonymize_vars(sorted_by_usage)

    var_list = get_var_list(sorted_by_usage, vc.expr_num)

    vt = VariableTransformer(var_list)

    return vt.visit(ast_tree)


def pipeline(code_string: str):
    return ast.unparse(clear_variables(ast.parse(code_string)))
