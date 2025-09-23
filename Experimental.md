
# Experimental Features and Extensions

The `mdsplus.ext` package provides features that in development, or otherwise not ready for prime time.

## GetManyMany

The `GetManyMany` class provides an interface for accessing many things from many shots. It will create up to `num_workers` threads with one `mdsthin.Connection` object each, and series of `GetMany` objects to complete all the queries. You can then iterate over the results as they come in.

```py
from mdsthin.ext import GetManyMany

gmm = GetManyMany(SERVER, num_workers=8)

gmm.append('y', '_sig = \\IP')
gmm.append('x', 'dim_of(_sig)')
# ...

gmm.add_shots(TREE, [ SHOTS...])
# ...

# Process the results one at a time
for result in gmm.execute():
    print(result.tree, result.shot)
    print(result.get('y').data())
    print(result.get('x').data())

# Or wait for them all to complete
all_results = list(gmm.execute())
```

When using `ssh://` or `sshp://`, you may need to put a small delay in-between each connection to avoid getting flagged as "too many connections appearing too quickly". If you find your connections are failing in this way, you can use the `worker_delay` argument to provide a delay in seconds.

```py
gmm = GetManyMany(SERVER, worker_delay=0.1)
```

## Tree

The `Tree` class approximates the regular `MDSplus.Tree` class, but layered on top of thin client. This means that properties such as `node.isWriteOnce()` will translate to expressions such as `conn.get('getnci($,"WRITE_ONCE")', nid)`, allowing you to (almost) seamlessly use the object-based API with mdsthin. While it is not possible to provide the full API, this should be a suitable replacement for most use cases. To create a `Tree` you first need a `Connection`, or at least a host to connect to. Here are the options for defining the connection to use:

* You can set `$MDS_HOST` which will be used to set the default connection automatically

```sh
export MDS_HOST=myserver
```

```py
from mdsthin.ext import Tree

t = Tree(TREE, SHOT)
# ...
```

* You can set a default connection

```py
from mdsthin import Connection
from mdsthin.ext import Tree, setDefaultConnection

c = Connection('myserver')
setDefaultConnection(c)

t = Tree(TREE, SHOT)
# ...
```

* You can pass the connection directly

```py
from mdsthin import Connection
from mdsthin.ext import Tree

c = Connection('myserver')

t = Tree(TREE, SHOT, conn=c)
# ...
```

These features are also available in the MDSplus compatibility package:

```py
from mdsthin import MDSplus

t = MDSplus.Tree(...)
# ...
``` 
