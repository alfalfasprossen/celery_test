This is just a test concerning module-level variables (used for caching data) and celery, as we ran into problems with this naïve approach in an actual project.

Our structure used was that a main-application would update and invalidate cached data depending on requests sent by clients, and issue tasks to operate on the same data.

We had problems with cached data suddenly being outdated, tasks depending on such data failing for strange reasons immediately, more or less randomly. The actual dropouts were not reproducible as far as we could see. Sometimes it worked, sometimes it didn't. Restarting the applications or the celery worker fixed the problem for a time (of course, deleting the cache), but that wasn't going to be a solution.

So we had to see in detail what celery is doing under the hood and how module-level variables are treated concerning cross-task and main-application-to-task behaviour.


### The observed results are:

The main-thread contains its own set of data, not shared with the worker or tasks in any way.

The worker has its own set of data, which (according to some comments on stackoverflow) is copied to each task-thread when that is created. So theoretically, changing data in the worker somehow would affect tasks created afterwards.

Each task has its own set of data, that is not synced across tasks. Modifications do not affect other tasks, do not affect the worker (spawning new tasks) and do not affect the main-application. 
Each task-thread keeps that data for as long as the worker is running. There is not a complete new set of data for each started task, just for each thread for the tasks. So if the worker runs with 8 threads, there are 8 seperate data blocks in memory.

So, updating the cache in the first task, and then reading the cache in the next task, won't have any visible effect, because the second task is executed on another thread.

effectively:

```
task1: cache=cache+1 (cache = 2)
task2: cache=cache+1 (cache = 2) Not 3!!!
task1: print cache: 2
task2: cache=cache+1 (cache = 3)
task1: print cache: 2 (still 2, because its on thread 1!)

```

This is the reason why we couldn't reproduce the dropouts. While one task thread might have an outdated cache at that point in time, another one might have an up-to-date cache, because it was created after a cache-update. Depending on which thread was chosen for the task, the cached data could be 'ok' or non-existent, resulting in what seemed to be random results.

### Verdict:
Caching on module level is technically impossible with celery tasks, unless the cache is cleared and built anew within each task, which doesn't make sense for all of our use-cases.

To use actual caching across tasks, and especially between the main-application and the tasks, a seperately running caching framework that can be reached from all of them through messages or so is necessary. Examples would be memcached or Redis or a database, etc.
