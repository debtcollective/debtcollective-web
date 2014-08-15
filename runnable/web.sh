#!/usr/bin/env bash
cd be && gunicorn proj.wsgi:application -b "0.0.0.0" -w 3 -k sync --preload --error-log=-