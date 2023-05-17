def foo1(arg1, arg2, arg3):
    arg1 += arg2
    arg3 /= arg1
    arg2 += arg3
    arg1 /= arg2
    arg3 += arg1
    var1 = arg1 + arg2 + arg3
    var2 = arg1 - arg2 - arg3
    var3 = var1 - var2
    return var3


def any_function1(a1: int, b1: int,
                  c1: int) -> (int, int, int):
    a1 += b1
    c1 /= a1
    b1 += c1
    a1 /= b1
    c1 += a1
    return a1, b1, c1

def any_function2(a2: int, b2: int,
                  c2: int) -> (int, int):
    d2 = a2 + b2 + c2
    e2 = a2 - b2 - c2
    return d2, e2

def any_function3(d3: int,
                  e3: int) -> int:
    f3 = d3 - e3
    return f3

def common_function(a: int, b: int,
                    c: int) -> int:
    a, b, c = any_function1(a, b, c)
    d, e = any_function2(a, b, c)
    f = any_function3(d, e)
    return f


def FUN_1(VAR_1: TYPE_1, VAR_2: TYPE_1,
          VAR_3: TYPE_1) -> TYPE_1:
    VAR_1 = VAR_1 + VAR_2
    VAR_3 = VAR_3 / VAR_1
    VAR_2 = VAR_2 + VAR_3
    VAR_1 = VAR_1 / VAR_2
    VAR_3 = VAR_3 + VAR_1
    VAR_4 = VAR_1 + VAR_2 + VAR_3
    VAR_5 = VAR_1 - VAR_2 - VAR_3
    VAR_6 = VAR_4 - VAR_5
    return VAR_6

