#!/bin/bash

gunicorn -c blog/gunicorn-config.py blog.wsgi
