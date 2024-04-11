from lookwhosstreaming.celery import app

@app.task(bind=True)
def task_function(self, *args, **kwargs):
    if args:
        print(f"Celery function from tasks.py, got args {args}, {kwargs}")
    else:
        print("This is a celery tasks.py function")