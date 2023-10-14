#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import django
from django.contrib.auth import get_user_model


def createSuperUser():
    django.setup()
    User = get_user_model()
    firstName = input("Enter first name: ")
    lastName = input("Enter last name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    User.objects.create_superuser(firstName=firstName,
                                  lastName=lastName,
                                  email=email,
                                  password=password)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if sys.argv[1] == 'createsuperuser':
        createSuperUser()
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
