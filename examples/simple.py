#
# Assumes a tree named 'thintest', with a structure of:
# :A
#   :B
#     :C
# \D -> A:B:C
#
# and some data in each node
#

import mdsthin

c = mdsthin.Connection('server')
c.openTree('thintest', 0)

a = c.get('A').data()
b = c.get('A.B').data()
c = c.get('A.B.C').data()
a = c.get('\\D').data()
