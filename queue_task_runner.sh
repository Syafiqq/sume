#!/usr/bin/env bash
celery -A sume worker -l info -c 1
