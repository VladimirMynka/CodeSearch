import typing
from tqdm import tqdm

from tree_sitter import Language, Parser, Tree, TreeCursor, Node
import pandas as pd

LANGUAGE = "java"
DATA_PATH = "../../data/java_train.csv"
COLUMNS = ['func1', 'func2']
DEBUG = False

TYPE_IDENTIFIER = "type_identifier"
ARRAY_TYPE = "integral_type"
IDENTIFIER = "identifier"
FUNC = "method_invocation"
ARGS = "argument_list"
VAR_DECLARE = "variable_declarator"
STR = "string_fragment"


def walk_and_get_variables(tree: Tree) -> tuple[list[typing.Any], list[Node]]:
    cursor: TreeCursor = tree.walk()
    nodes_order = []
    nodes_flat = []
    parents = [nodes_order]
    while True:
        if cursor.node.child_count > 0:
            current = [cursor.node]
            nodes_flat.append(cursor.node)
            parents[-1].append(current)
            parents.append(current)
            cursor.goto_first_child()
        else:
            current = [cursor.node, []]
            parents[-1].append(current)

            nodes_flat.append(cursor.node)
            while cursor.node.next_sibling is None:
                if cursor.node.parent is None:
                    return nodes_order, nodes_flat

                cursor.goto_parent()
                parents = parents[:-1]
            cursor.goto_next_sibling()


def type_getter(nodes_flat: list[Node]) -> list[Node]:
    return [node for node in nodes_flat if (node.type == TYPE_IDENTIFIER) or (node.type == ARRAY_TYPE)]


def func_getter(nodes_flat: list[Node]) -> list[Node]:
    return [node for node in nodes_flat if
            (node.type == IDENTIFIER) and ((
                                               (node.parent.type == FUNC) and (node.next_sibling.type == ARGS)
                                           ) or (
                                               (node.parent.type == VAR_DECLARE) and (node.next_sibling is None)
                                           ))]


def var_getter(nodes_flat: list[Node]) -> list[Node]:
    return [node for node in nodes_flat if
            (node.type == IDENTIFIER) and not ((
                                                   (node.parent.type == FUNC) and (node.next_sibling.type == ARGS)
                                               ) or (
                                                   (node.parent.type == VAR_DECLARE) and (node.next_sibling is None)
                                               ))]


def str_getter(nodes_flat: list[Node]) -> list[Node]:
    return [node for node in nodes_flat if (node.type == STR)]


def replace_anything(parser, code_fragment, nodes_getter, prefix, debug=False) -> str:
    tree = parser.parse(bytes(code_fragment, 'utf-8'))
    nodes_tree, nodes_flat = walk_and_get_variables(tree)

    nodes = nodes_getter(nodes_flat)
    if debug:
        print('\n'.join([str(node) + bytes.decode(node.text) for node in nodes]))
        print('\n')

    i = 0
    mapper = {}
    for node in nodes:
        if node.text in mapper:
            continue
        mapper[node.text] = f"{prefix}_{i}"
        i += 1

    shift = 0

    for node in nodes:
        start = node.start_byte + shift
        end = node.end_byte + shift

        code_fragment = code_fragment[:start] + mapper[node.text] + code_fragment[end:]

        shift += len(mapper[node.text]) - len(node.text)

    return code_fragment


def replace_types(parser: Parser, code_fragment: str, debug: bool = False) -> str:
    return replace_anything(parser, code_fragment, type_getter, "TYPE", debug)


def replace_funcs(parser: Parser, code_fragment: str, debug: bool = False) -> str:
    return replace_anything(parser, code_fragment, func_getter, "FUNC", debug)


def replace_vars(parser: Parser, code_fragment: str, debug: bool = False) -> str:
    return replace_anything(parser, code_fragment, var_getter, "VAR", debug)


def replace_strs(parser: Parser, code_fragment: str, debug: bool = False) -> str:
    return replace_anything(parser, code_fragment, str_getter, "ANY_TEXT", debug)


def replace(parser: Parser, code_fragment: str, debug: bool = False) -> str:
    code_fragment = replace_types(parser, code_fragment, debug)
    code_fragment = replace_funcs(parser, code_fragment, debug)
    code_fragment = replace_vars(parser, code_fragment, debug)
    code_fragment = replace_strs(parser, code_fragment, debug)
    return code_fragment


def init_parser():
    language = Language('build/my-languages.so', LANGUAGE)
    parser = Parser()
    parser.set_language(language)

    return parser


def main():
    data = pd.read_csv(DATA_PATH)
    parser = init_parser()

    def replacer(fragment):
        return replace(parser, fragment, DEBUG)

    for column in tqdm(COLUMNS):
        data[f"{column}_norm"] = data[column].apply(replacer)

    data.to_csv(f"{DATA_PATH[:-4]}_normalized.csv")


if __name__ == "__main__":
    main()
