class UnitsMismatch (TypeError):
    """Represents binary operations on incompatible unit dimensions."""
    def __init__(self, tmpl, *a):
        TypeError.__init__(self, tmpl.format(*a))


class BaseParseError (ValueError):
    def __init__(self, tmpl, *args, **kw):
        ValueError.__init__(self, tmpl.format(*args, **kw))


class UnitsParseError (BaseParseError):
    pass


class ValueParseError (BaseParseError):
    pass
