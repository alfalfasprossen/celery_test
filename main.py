from celery_test import cache
from celery_test import tasks

while True:
    cmd = raw_input("'task_checkcache' or "
                    "'task_bumpcache' or "
                    "'main_printcache'")
    if cmd == 'task_checkcache':
        tasks.check_cache.delay()
    if cmd == 'task_bumpcache':
        tasks.bump_cache.delay()
    if cmd == 'main_printcache':
        print 'main cache is: {}'.format(cache.cached_var)
