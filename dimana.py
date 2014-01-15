# Copyright 2014 Nathan Wilcox
#
# This file is distributed under the terms of the TGPPL v. 1.0 found
# in ./COPYING.TGPPL.rst.

"""_Dim_ensional _Ana_lysis - Values with associated measurement units.

Example:
>>> from dimana import Dimensional

>>> Feet = Dimensional.get_dimension('Feet')
>>> Lbs = Dimensional.get_dimension('Lbs')
>>> Sec = Dimensional.get_dimension('Sec')

>>> Feet(23) * Lbs(13) / (Sec(1) * Sec(1))
299 [(Feet*Lbs) / Sec^2]
"""

from decimal import Decimal


class Dimensional (object):
    # Warning: This assumes subclass names are unique across the runtime.

    @staticmethod
    def get_dimension(name):
        return Dimensional._get_multi( {name: 1} )

    @staticmethod
    def _get_multi(dims):
        key = 'Dimensional_' + '_'.join( '%s_%s' % p for p in sorted(dims.items())).replace('-','_')

        try:
            return Dimensional._subtype_cache[key]
        except KeyError:
            subtype = Dimensional._define_new(key, dims)
            Dimensional._subtype_cache[key] = subtype

            # Constants:
            subtype.zero = subtype('0.0')
            subtype.one = subtype('1.0')

            return subtype

    @staticmethod
    def _define_new(name, dims):
        return type(name, (Dimensional,), {'_dims': dims})

    _subtype_cache = {}

    _dims = {}

    def __init__(self, value):
        self.value = Decimal(value)

    @property
    def dimstr(self):
        poses = []
        negs = []
        for (unit, power) in self._dims.iteritems():
            assert power != 0, `self._dims`
            abspower = abs(power)

            s = unit
            if abspower != 1:
                s += '^%d' % abspower

            if power > 0:
                poses.append(s)
            else:
                negs.append(s)

        posstr = '*'.join(poses)
        negstr = '*'.join(negs)
        if negs:
            if poses:
                if len(poses) > 1:
                    posstr = '(%s)' % (posstr,)
            else:
                posstr = '1'
            if len(negs) > 1:
                negstr = '(%s)' % (negstr,)

            result = '%s / %s' % (posstr, negstr)
        else:
            result = posstr
        return '[%s]' % (result,)

    @property
    def inverse(self):
        return self.inverseunits( Decimal(1) / self.value )

    @property
    def inverseunits(self):
        return type(self)._get_multi(dict( (k, -v) for (k, v) in self._dims.iteritems() ))

    def __repr__(self):
        return '%s %s' % (self.value, self.dimstr)

    def __cmp__(self, other):
        typecheck(other, type(self))
        return cmp(self.value, other.value)

    def __add__(self, other):
        typecheck(other, type(self))
        return type(self)(self.value + other.value)

    def __sub__(self, other):
        return self + ( - other )

    def __neg__(self):
        return type(self)( - self.value )

    def __mul__(self, other):
        typecheck(other, Dimensional)

        dims={}
        for key in set(self._dims.keys() + other._dims.keys()):
            sumpower = self._dims.get(key, 0) + other._dims.get(key, 0)
            if sumpower != 0:
                dims[key] = sumpower

        cls = Dimensional._get_multi(dims)
        return cls(self.value * other.value)

    def __pow__(self, p):
        if p == 1.0:
            return self
        elif p == 0:
            # NOTE: Without this special case, Decimal('0') ** 0 raises an exception.
            return Dimensional.one
        else:
            dims={}
            for (unit, power) in self._dims.items():
                powerpower = power * p
                if powerpower != 0:
                    dims[unit] = powerpower

            cls = Dimensional._get_multi(dims)
            return cls(self.value ** p)

    def __div__(self, other):
        return self * other.inverse

Dimensional.zero = Dimensional('0.0')
Dimensional.one = Dimensional('1.0')


def typecheck(i, t):
    if not isinstance(i, t):
        raise TypeError('Type %r does not include instance %r' % (t, i))

