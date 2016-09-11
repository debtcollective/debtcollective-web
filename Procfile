web: cd be && newrelic-admin run-program gunicorn proj.wsgi --log-file -
worker: cd be && export DJANGO_SETTINGS_MODULE=proj.settings && celery worker --app=proj.arcs.dtr.app --loglevel=INFO