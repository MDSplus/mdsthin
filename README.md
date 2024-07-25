
# mdsthin - Python MDSplus Thin Client Implementation

This package provides the types and functions needed to interface with MDSplus over thin client. This contains most of the functionality from the regular MDSplus C+Python package, but does not map perfectly. If you are migrating from the regular package, or plan to support both, see [Full MDSplus Package Compatability](#full-mdsplus-package-compatability).

**What is thin client?**  
Thin allows access to MDSplus through TDI expressions, using the `Connection` class in python, or `mdsconnect`/`mdsvalue` in our other APIs.

## Installation

```sh
python3 -m pip install mdsthin
```

## Examples

See the [`examples`](examples/) folder.

## Tests

You can run the full test suite with:

```sh
python3 -m mdsthin.test [-v] [--server SERVER] [--cmod]
```

Or use it from a python prompt

```py
from mdsthin import test

test.run_mdsthin_tests(server='SERVER')
```

## Usage

```py
import mdsthin
```

### Connect to a server

```py
# Connect over MDSip
c = mdsthin.Connection('server')

# Specify a custom username and port for MDSplus
c = mdsthin.Connection('username@server:8123')

# Connect over SSH
c = mdsthin.Connection('ssh://server')
c = mdsthin.Connection('sshp://server')
```

For more information on how to use MDSip over SSH, see [Advanced SSH Usage](#advanced-ssh-usage)

### Run TDI expressions

```py
c.get('whoami()').data() # "username"

c.get('getenv("HOSTNAME")').data() # "server"

# Using argument substitution
c.get('4 + $', 5) # 9Q
```

### Run TCL commands

```py
print(c.tcl('show current test'))
# Current shot is 123

# Create a new pulse
c.tcl('set tree test /shot=-1')
c.tcl('create pulse 123')
```

This is just a wrapper function around the TDI `Tcl()` function.

### Open/Close Trees

```py
# Open the current shot
c.openTree('test', 0)

# Open or close a specific shot
c.openTree('test', 123)
c.closeTree('test', 123)

# Close all open trees
c.closeAllTrees()
```

### Read data from nodes

You will want to call `.data()` on the result of almost every `.get()` command. When you call `.get()` you will retrieve the MDSplus type, such as `Int32` or `Float32Array`. When you call `.data()` on these objects, you get the native numpy data type such as `numpy.int32` or `numpy.ndarray(dtype='float32')`.

```py
c.openTree('test', 0)

# Read individual nodes
y = c.get('SIGNAL_NODE').data()
x = c.get('dim_of(SIGNAL_NODE)').data()

# Read multiple nodes at the same time
gm = c.getMany()
gm.append('y', 'SIGNAL_NODE')
gm.append('x', 'dim_of(SIGNAL_NODE)')
gm.execute()

y = gm.get('y').data()
x = gm.get('x').data()

# Read the entire object
sig = c.getObject('SIGNAL_NODE').data()
y = sig.data()
x = sig.dim_of()

# Read data from tags
ip = c.get('\\IP').data()

# Read data from nodes inside other nodes
freq = c.get('HARDWARE.DEVICE.FREQUENCY')
seglen = c.get('HARDWARE.DEVICE.SEGLEN')
amp = c.get('HARDWARE.DEVICE.AMPLITUDE')

# Or set the default node to make this easier
# (This is similar to the `cd` shell command)
c.setDefault('HARDWARE.DEVICE')

freq = c.get('FREQUENCY')
seglen = c.get('SEGLEN')
amp = c.get('AMPLITUDE')

# Reset the default back to the top
c.setDefault('\\TOP')
```

### Writing data into nodes

```py
c.openTree('test', -1)

# Using a TDI expression
c.put('HARDWARE.DEVICE.FREQUENCY', '10000.')

# Using a python type
c.put('HARDWARE.DEVICE.FREQUENCY', '$', 10000.0)

# Using an explicit MDSplus type
c.put('HARDWARE.DEVICE.FREQUENCY', '$', mdsthin.Float32(10000.0))

# Writing to multiple nodes at once
pm = c.putMany()
pm.append('HARDWARE.DEVICE.FREQUENCY', '$', 10000.0)
pm.append('HARDWARE.DEVICE.SEGLEN', '$', 8000)
pm.append('HARDWARE.DEVICE.AMPLITUDE', '$', 5.0)
pm.execute()

# Writing objects using TDI expressions
c.put('INIT_THING', 'Build_Action(Build_Dispatch(0, "THING", "INIT", 50, ""), do_thing(), "")')

# Writing objects using serialize
from mdsthin import *
init_action = Action(Dispatch(0, 'THING', 'INIT', 50, ''), EXT_FUNCTION(None, 'do_thing'), '', )
c.put('INIT_THING', 'SerializeIn($)', init_action.serialize())
```

## A remote `mdstcl` prompt using `mdsthin.mdstcl`

This will let you run TCL commands and view their output.

Unfortunately, command history is not supported 🙁.

```
python3 -m mdsthin.mdstcl SERVER
Connectiong to: SERVER
TCL> show current test
123
TCL> exit
```

Or use it from a python prompt

```py
import mdsthin
c = mdsthin.Connection('server')

c.mdstcl()
TCL> show current test
123
TCL> exit
```

This can be very useful to interactively work with a tree. **Note:** any trees you open will affect the entire connection, and calling `set default xyz` will have the same effect as calling `c.setDefault('xyz')`.

## A remote `tdic` prompt using `mdsthin.tdic`

This will let you run TDI expressions and view their output.

Unfortunately, command history is not supported 🙁.

```
python3 -m mdsthin.tdic SERVER
Connectiong to: SERVER
TDI> 4 + 5
9L
TDI> exit
```

Or use it from a python prompt

```py
import mdsthin
c = mdsthin.Connection('server')

c.tdic()
TDI> 4 + 5
9L
TDI> exit
```

## Full MDSplus Package Compatability

For those coming from the regular `MDSplus` package, or who want to ensure they do not use functionality from `mdsthin` that is not present in the regular `MDSplus` package, we provide a subpackage called `MDSplus`.

This provides a better mapping to the regular `MDSplus` package by:
* Adding functions to approximate functionality missing in `mdsthin`
* Removing types/functions not present in the regular `MDSplus` package
* Aliasing types that are not directly present in `mdsthin`

```py
from mdsthin import MDSplus

c = MDSplus.Connection('server')

i = Uint32(42)

MDSplus.mdsExceptions.checkStatus(265388200)
```

If you encounter code that should work with this package but doesn't, please [create an issue](https://github.com/MDSplus/mdsthin/issues/new) and we'll do our best to provide compatability.

## Advanced SSH Usage

There are two methods of SSH supported, `ssh://` and `sshp://`.

Using `ssh://` will attempt to spawn `/bin/sh -l -c mdsip-server-ssh` on the remote server, and then use that as the MDSip server.

**Note:** This will fail if you do not source the MDSplus `setup.sh` on login, or if it cannot find `mdsip-server-ssh` on the `$PATH`.

Using `sshp://` will attempt to spawn `nc PROXY_HOST PROXY_PORT` on the remote server, and then use that to proxy to the MDSip server. You can configure the `PROXY_HOST` and `PROXY_PORT` when creating a `Connection` by passing `ssh_proxy_host` and `ssh_proxy_port`.

```py
# Specify a custom username and port for SSH
c = mdsthin.Connection('ssh://username@server:2222')

# Proxy to a given host and port
c = mdsthin.Connection('sshp://proxy-server',
    sshp_host='server', sshp_port=8123)

# Specify additional SSH command line options
c = mdsthin.Connection('ssh://server',
    ssh_subprocess_args=['-i', '/path/to/private/key'])

# The default backend for SSH is 'subprocess', which executes `ssh`
# in a subprocess.Popen(), we also support the paramiko package
# for pure-python SSH connections
c = mdsthin.Connection('ssh://server', ssh_backend='paramiko')

# Specify additional kwargs to paramiko's `connect()` function
import paramiko
key = paramiko.RSAKey.from_private_key_file("/path/to/private/key")

c = mdsthin.Connection('ssh://server', ssh_backend='paramiko',
    ssh_paramiko_options={ 'pkey': key })
```
