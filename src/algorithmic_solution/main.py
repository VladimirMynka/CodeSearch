import inspect

from src.algorithmic_solution.algorithms import rename_variables_pipeline, explode_functions_pipeline
from src.algorithmic_solution.utils import get_ctx

import src.algorithmic_solution.test as test


if __name__ == "__main__":
    x = inspect.getsource(test.common_function)
    x = explode_functions_pipeline(x, get_ctx(vars(test).items()))

    print(x)
    x = rename_variables_pipeline(x)
    print(x)
