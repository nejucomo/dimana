
class Units (object):
    def __new__(cls, dimpowers):
        dpkey = tuple(sorted(dimpowers.iteritems()))
        inst = cls._instances.get(dpkey)
        if inst is None:
            inst = super(Units, cls).__new__(cls, dimpowers)
            cls._instances[dpkey] = inst
        return inst

    def __init__(self, dimpowers):
        if not hasattr(self, '_dimpowers'):
            self._dimpowers = dimpowers
        # Else: this instance has already been initialized.

    def __mul__(self, other):
        if isinstance(other, Units):
            newdp = {}

            def set_dp(n, p):
                assert n not in newdp, repr((newdp, n, p))
                if p != 0:
                    newdp[n] = p

            tmpdp = dict(self._dimpowers)
            for uname, power in other._dimpowers.iteritems():
                set_dp(uname, power + tmpdp.pop(uname, 0))
            for uname, power in tmpdp.iteritems():
                set_dp(uname, power)
            return Units(newdp)
        else:
            raise TypeError(
                'Units multiplied against non-Units {!r}'
                .format(type(other))
            )

    def __div__(self, other):
        return self * (other ** -1)

    __truediv__ = __div__

    def __pow__(self, p):
        newdp = {}
        if p != 0:
            for uname, power in self._dimpowers.iteritems():
                newdp[uname] = power * p
        return Units(newdp)

    # Private:
    _instances = {}


Units.scalar = Units({})
