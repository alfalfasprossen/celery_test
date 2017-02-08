from __future__ import absolute_import

from celery import Celery


app = Celery('celery_test',
             broker='pyamqp://guest@localhost//',
             include=['celery_test.tasks'])


if __name__ == '__main__':
    app.start()
