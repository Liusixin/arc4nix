import sys
import functools
import uuid
from pprint import pprint as pp

me = sys.modules[__name__]

__on_windows__ = sys.platform.find("win") != -1

__all__ = ['add_predefined_statement', 'map_path_var', 'predefined_block']

__all_functions__ = {
    'analysis': ['Buffer', 'Clip', 'Erase', 'Identity', 'Intersect', 'SymDiff', 'Update', 'Split', 'Near',
                 'PointDistance', 'Select', 'TableSelect', 'Frequency', 'Statistics', 'CreateThiessenPolygons',
                 'SpatialJoin', 'MultipleRingBuffer', 'GenerateNearTable', 'Union', 'TabulateIntersection',
                 'PolygonNeighbors']
}

__path_expr_holder__ = []

predefined_block = []

def add_predefined_statement(statement):
    if isinstance(statement, basestring):
        predefined_block.append(statement)
        

def map_path_var(in_path):
    var_name = "p_" + str(uuid.uuid4()).replace("-", "_")
    # Use base64 encoded value, remove trailing "\n"
    return var_name + "<-path|b64|" + in_path.encode("base64").rstrip(), var_name


def fix_paths_args(arg, force_repr=__on_windows__):
    if force_repr:
        return repr(arg)
    arg_repr = []
    # if args is list, recursively goes inside
    if isinstance(arg, list):
        sub_arg = map(fix_paths_args, arg)
        arg_repr.append("[%s]" % ",".join(sub_arg))
    elif isinstance(arg, tuple):
        sub_arg = map(fix_paths_args, arg)
        arg_repr.append("(%s)" % ",".join(sub_arg))    
    # TODO: if args is arcpy4nix.Raster dummpy class, return its path
    # These are typically paths
    
    # A path firstly must be a string
    elif isinstance(arg, basestring):
        is_path = False
        if arg.startswith("path:"):
            is_path = True
            arg = arg[5:]
        elif arg.startswith("/") or arg.startswith("./") or arg.startswith("../"):
            is_path = True
        if is_path:
            path_expr, path_var = map_path_var(arg)
            __path_expr_holder__.append(path_expr)
            arg_repr.append(path_var)
        else:
            arg_repr.append(repr(arg))
    else:
        arg_repr.append(repr(arg))
    
    return ",".join(arg_repr)

def fix_paths_kwargs(kwarg, force_repr=__on_windows__):
    var, arg = kwarg
    return '%s=%s' % (var, repr(arg) if force_repr else fix_paths_args(arg))


def send_wrap(name, *args, **kwargs):
    variable_sent = ";".join(__path_expr_holder__)
    func_str = create(name, *args, **kwargs)
    print(func_str)


def create(name, *args, **kwargs):
    global __path_expr_holder__
    __path_expr_holder__ = []
    expr = name + "("
    if args:
        # list args
        new_args = map(fix_paths_args, args)
        expr += ", ".join(new_args)                                                                     
    if kwargs:
        if args:
            expr += ", "
        # kw args
        new_kwargs = map(fix_paths_kwargs, kwargs.items())
        expr += ", ".join(new_kwargs)
    expr += ")"
    return repr(expr)


for cat, func_list in __all_functions__.items():
    for func_stub in func_list:
        func_name = "%s_%s" % (func_stub, cat)
        # We need actually do something tricky.
        setattr(me, func_name, functools.partial(send_wrap, func_name))
        __all__.append(func_name)

del me