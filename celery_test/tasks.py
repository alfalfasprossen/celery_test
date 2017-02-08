from __future__ import absolute_import

from .celery import app

from celery_test import cache


@app.task
def check_cache():
    print 'task cache is: {}'.format(cache.cached_var)


@app.task
def bump_cache():
    cache.cached_var += 1
    print 'upped task cache: {}'.format(cache.cached_var)
