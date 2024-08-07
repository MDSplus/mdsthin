
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