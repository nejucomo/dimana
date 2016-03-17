from decimal import Decimal
from dimana.typecheck import typecheck
from dimana.units import Units


class Value (object):
    def __init__(self, decimal, units):
        typecheck(decimal, Decimal)
        typecheck(units, Units)

        self.decimal = decimal
        self.units = units

    def __str__(self):
        return '{} [{}]'.format(self.decimal, self.units)

    def __repr__(self):
        return '<{} {!r}>'.format(type(self).__name__, str(self))
