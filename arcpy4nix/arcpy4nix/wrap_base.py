import sys
import functools

me = sys.modules[__name__]

__all__ = []

__all_functions__ = {
    'analysis': ['Buffer', 'Clip', 'Erase', 'Identity', 'Intersect', 'SymDiff', 'Update', 'Split', 'Near',
                 'PointDistance', 'Select', 'TableSelect', 'Frequency', 'Statistics', 'CreateThiessenPolygons',
                 'SpatialJoin', 'MultipleRingBuffer', 'GenerateNearTable', 'Union', 'TabulateIntersection',
                 'PolygonNeighbors']
}


def fix_paths_args(arg):
    return None, repr(arg)


def fix_paths_kwargs(kwarg):
    var, arg = kwarg
    return None, '%s=%s' % (var, repr(arg))


def create(name, *args, **kwargs):
    expr = name + "("
    if args:
        # list args
        # TODO: Path fix
        path_vars, new_args = zip(*map(fix_paths_args, args))
        expr += ", ".join(new_args)
    if kwargs:
        expr += ", "
        # kw args
        # TODO: Path fix
        path_vars2, new_kwargs = zip(*map(fix_paths_kwargs, kwargs.iteritems()))
        expr += ", ".join(new_kwargs)
    expr += ")"

    print(name)
    print(args)
    print(kwargs)
    print repr(expr)



for cat, func_list in __all_functions__.iteritems():
    for func_stub in func_list:
        func_name = "%s_%s" % (func_stub, cat)
        # We need actually do something tricky.
        setattr(me, func_name, functools.partial(create, func_name))
        __all__.append(func_name)
