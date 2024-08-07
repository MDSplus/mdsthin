
import time
import queue
import threading

from ..connection import Connection
from ..exceptions import getExceptionFromError

class GetManyMany:

    class Result:

        def __init__(self, tree, shot, result):
            self._tree = tree
            self._shot = shot
            self._result = result

        @property
        def tree(self):
            return self._tree

        @property
        def shot(self):
            return self._shot

        def get(self, name):
            
            if name not in self._result:
                return None
            
            result = self._result[name]
            if 'value' in result:
                return result['value']
            
            raise getExceptionFromError(result['error'].data())

    class Worker(threading.Thread):

        def __init__(self, gmm):
            super().__init__()

            self._gmm = gmm

        def run(self):

            c = Connection(self._gmm._connection_url, **self._gmm._connection_kwargs)

            while True:
                try:
                    tree, shot = self._gmm._shots.get_nowait()
                except queue.Empty:
                    break

                gm = c.getMany()
                gm.append('_gmm_open', 'TreeOpen($,$)', tree, shot)

                for query in self._gmm._queries:
                    gm.append(query['name'], query['exp'], *query['args'])

                result = gm.execute()
                
                self._gmm._results.put(GetManyMany.Result(tree, shot, result))

            c.disconnect()

    def __init__(self, connection_url: str, num_workers: int = 8, worker_delay: float = 0.0, **connection_kwargs):
        
        self._connection_url = connection_url
        self._connection_kwargs = connection_kwargs
        self._num_workers = num_workers
        self._worker_delay = worker_delay

        self._total_shots = 0
        self._shots = queue.Queue()
        self._results = queue.Queue()
        self._queries = []
        self._workers = []

    def add_shots(self, tree, shots):
        if not isinstance(shots, list):
            shots = [ shots ]
        
        for shot in shots:
            self._shots.put((tree, shot))
            self._total_shots += 1

    def append(self, name, exp, *args):
        self._queries.append({
            'name': name,
            'exp': exp,
            'args': list(args),
        })

    def execute(self):
        
        num_workers = min(self._num_workers, self._total_shots)
        for _ in range(num_workers):
            worker = self.Worker(self)
            worker.start()

            if self._worker_delay > 0:
                time.sleep(self._worker_delay)

            self._workers.append(worker)

            # If the previous threads have already finished, don't make new ones
            if self._shots.qsize() == 0:
                break
        
        for _ in range(self._total_shots):
            yield self._results.get()
        
        for worker in self._workers:
            worker.join()
