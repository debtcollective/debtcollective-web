#!/usr/bin/env bash
cd be && celery worker -l INFO --app=proj.celery_settings