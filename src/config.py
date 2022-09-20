import os
import json
import multiprocessing

bind = f"0.0.0.0:{os.environ.get('BACKEND_PORT', 8000)}"
workers = os.environ.get('MATCHER_APP_WORKERS', 1)
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
thread = os.environ.get('WORKERS_THREAD', 2 * multiprocessing.cpu_count())
loglevel = "debug" if json.loads(os.environ.get('DEBUG', "False").lower()) else "info"
