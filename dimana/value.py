import re
from decimal import Decimal
from dimana.typecheck import typecheck
from dimana.units import Units


class Value (object):

    class ParseError (ValueError):
        pass

    @classmethod
    def parse(cls, text):
        m = cls._rgx.match(text)
        if m is None:
            raise cls.ParseError('Could not parse Value: {!r}'.format(text))

        decimal = Decimal(m.group(1))
        units = Units.parse(m.group(2))
        return cls(decimal, units)

    def __init__(self, decimal, units):
        typecheck(decimal, Decimal)
        typecheck(units, Units)

        self.decimal = decimal
        self.units = units

    def __str__(self):
        return '{} [{}]'.format(self.decimal, self.units)

    def __repr__(self):
        return '<{} {!r}>'.format(type(self).__name__, str(self))

    # Private
    _rgx = re.compile(r'^(\S+) +\[(.*?)\]$')
