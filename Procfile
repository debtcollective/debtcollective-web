web: cd be && newrelic-admin run-program gunicorn proj.wsgi --log-file -
worker: cd be && celery worker --app=proj.arcs.dtr.app --loglevel=INFO