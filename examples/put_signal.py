#
# Assumes a tree named 'thintest', with a structure of:
# :SIG
#

import math
import numpy
import mdsthin

c = mdsthin.Connection('server')
c.openTree('thintest', 0)

data = numpy.array([ math.sin(theta * 0.1) for theta in range(0, 10) ])
times = numpy.array(list(range(10)))

sig = mdsthin.Signal(data, None, times)

# Signals cannot be written directly like scalars or arrays, so we need to serialize/deserialize it
c.put('SIG', 'SerializeIn($)', sig.serialize())
