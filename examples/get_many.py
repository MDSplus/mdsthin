#
# Assumes a tree named 'thintest', with a structure of:
# :TITLE
# :SIG
#
# a String in TITLE, and a Signal in SIG
#

import mdsthin

c = mdsthin.Connection('server')
c.openTree('thintest', 0)

gm = c.getMany()
gm.append('title', 'TITLE')
gm.append('y', 'SIG')
gm.append('x', 'dim_of(SIG)')
gm.execute()

title = gm.get('title').data()
y = gm.get('y').data()
x = gm.get('x').data()

from matplotlib import pyplot
pyplot.title(title)
pyplot.plot(x, y)
pyplot.show()