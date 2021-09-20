from celery import group
from celery import task


@app.task
def mult(f):
        return f**f



fd = [1, 2, 3]

jobs = group(mult.s(f) for item in fd)
result = jobs.apply_async()