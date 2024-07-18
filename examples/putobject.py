#
# Assumes a tree named 'thintest', with a structure of:
# :DO_THING
#
# and some data in each node
#

import mdsthin

c = mdsthin.Connection('server')
c.openTree('thintest', 0)

a = mdsthin.Action(
    mdsthin.Dispatch(0, 'THING', 'INIT', 50, ''),
    mdsthin.EXT_FUNCTION(None, 'thing_method'),
    '',
    None,
    None
)

a = c.put('DO_THING', 'SerializeIn($)', a.serialize())
