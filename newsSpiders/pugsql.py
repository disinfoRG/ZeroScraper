import pugsql


def add_query(queries, stmt):
    """
    Dynamically add queries to pugsql modules.  A hack.
    """
    s = pugsql.parser.parse(stmt, ctx=None)
    if hasattr(queries, s.name):
        raise ValueError('Please choose another name than "%s".' % s.name)
    s.set_module(queries)
    setattr(queries, s.name, s)
    queries._statements[s.name] = s


def module(*args, **kwargs):
    queries = pugsql.module(*args, **kwargs)
    queries.add_query = add_query.__get__(queries)
    return queries
