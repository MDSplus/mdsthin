
# mdsthin - Python MDSplus Thin Client Implementation

## Installation

```sh
python3 -m pip install mdsthin
```

## Tests

```sh
python3 -m mdsthin.test [-v] [--server SERVER] [--cmod]
```

## Usage

```py
import mdsthin
c = mdsthin.Connection('server')


print(c.get('whoami()').data())
# username

print(c.tcl('show current test'))
# 123

print(c.get('4 + 5').data())
# 9


c.openTree('test', 123)


y = c.get('SIGNAL_NODE').data()
x = c.get('dim_of(SIGNAL_NODE)').data()


gm = c.getMany()
gm.append('y', 'SIGNAL_NODE')
gm.append('x', 'dim_of(SIGNAL_NODE)')
gm.execute()

y = gm.get('y').data()
x = gm.get('x').data()


print(c.getObject('ACTION_NODE').data())
# Action(...)


# Build_Signal(1000. * $VALUE, Word_Unsigned([1,2,3,4,5]), [0QU,10QU,20QU,30QU,40QU])
Signal(MULTIPLY(Float32(1000.0), dVALUE()), UInt16Array([1, 2, 3, 4, 5]), UInt64Array([0, 10, 20, 30, 40]))

```

## Examples

See the `examples/` folder.

## mdstcl

```
python3 -m mdsthin.mdstcl SERVER
Connectiong to: SERVER
TCL> show current test
123
TCL> exit
```

```py
import mdsthin
c = mdsthin.Connection('server')

c.mdstcl()
TCL> show current test
123
TCL> exit
```

## tdic

```
python3 -m mdsthin.tdic SERVER
Connectiong to: SERVER
TDI> 4 + 5
9L
TDI> exit
```

```py
import mdsthin
c = mdsthin.Connection('server')

c.tdic()
Connectiong to: SERVER
TDI> 4 + 5
9L
TDI> exit
```

## Compatability with full MDSplus python package

There is a subpackage called `MDSplus` that provides slightly better mappings with the full MDSplus python package.

```py
from mdsthin import MDSplus

c = MDSplus.Connection('server')

i = Uint32(42)

MDSplus.mdsExceptions.checkStatus(265388200)
```