"""Gunicorn settings (used by deploy/rezume.service)."""

import multiprocessing

bind = "127.0.0.1:8000"
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)
timeout = 30
graceful_timeout = 20
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
accesslog = "-"
errorlog = "-"
loglevel = "info"
forwarded_allow_ips = "127.0.0.1"
