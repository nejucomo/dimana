
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

    # Private:
    _instances = {}
