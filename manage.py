#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

import speckenv


if __name__ == "__main__":
    speckenv.read_speckenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmmoney.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
