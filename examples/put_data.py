#
# Assumes a tree named 'thintest', with a structure of:
# :A
# :B
# :C
#

import numpy
import mdsthin

c = mdsthin.Connection('server')
c.openTree('thintest', 0)

c.put('A', '$', 42)

c.put('B', '$', "hello world")

data = numpy.array([ 0.0, 0.1, 0.2, 0.3 ])
c.put('C', '$', data)
