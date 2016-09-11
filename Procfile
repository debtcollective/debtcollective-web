web: cd be && newrelic-admin run-program gunicorn proj.wsgi --log-file -
worker: celery worker --app=be.proj.arcs.tasks.app