#
# Assumes a tree named 'thintest', with a structure of:
# :DO_THING
#
# and an Action in DO_THING
#

import mdsthin

c = mdsthin.Connection('server')
c.openTree('thintest', 0)

a = c.getObject('DO_THING')
print(a.dispatch)
print(a.task)
print(a.errorlogs)
print(a.completion_message)
print(a.performance)
