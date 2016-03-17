import re
from functools import wraps
from decimal import Decimal, InvalidOperation
from dimana import exc
from dimana.typecheck import typecheck
from dimana.units import Units


# Private Units-matching decorator:
def units_must_match(method):

    @wraps(method)
    def m(self, other):
        typecheck(other, Value)
        self.units.match(other.units)
        return method(self, other)
    return m


class Value (object):

    class ParseError (exc.ParseError):
        pass

    @classmethod
    def parse(cls, text):
        m = cls._rgx.match(text)
        if m is None:
            raise cls.ParseError('Could not parse Value: {!r}', text)

        dectext = m.group(1)
        try:
            decimal = Decimal(dectext)
        except InvalidOperation as e:
            raise cls.ParseError(
                'Could not parse decimal {!r} of Value: {}',
                dectext,
                e,
            )

        units = Units.parse(m.group(2))
        return cls(decimal, units)

    def __init__(self, decimal, units):
        typecheck(decimal, Decimal)
        typecheck(units, Units)

        self.decimal = decimal
        self.units = units

    # str/repr Methods:
    def __str__(self):
        return '{} [{}]'.format(self.decimal, self.units)

    def __repr__(self):
        return '<{} {!r}>'.format(type(self).__name__, str(self))

    # Arithmetic Methods:
    @units_must_match
    def __cmp__(self, other):
        return cmp(self.decimal, other.decimal)

    def __pos__(self):
        return self

    def __neg__(self):
        return Value(-self.decimal, self.units)

    @units_must_match
    def __add__(self, other):
        return Value(self.decimal + other.decimal, self.units)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        typecheck(other, Value)
        return Value(self.decimal * other.decimal, self.units * other.units)

    def __div__(self, other):
        typecheck(other, Value)
        return Value(self.decimal / other.decimal, self.units / other.units)

    def __pow__(self, other, modulus=None):
        if modulus is None:
            return Value(self.decimal ** other, self.units ** other)
        else:
            raise TypeError('Modulus not supported for {!r}', self)

    # Private
    _rgx = re.compile(r'^(\S+) +\[(.*?)\]$')
