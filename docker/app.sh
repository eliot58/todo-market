#!/bin/bash

gunicorn --bind 0.0.0.0:6000 market.wsgi