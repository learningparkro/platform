#!/usr/bin/env python

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/get_num_users_for_permission.py

import sys
import csv
import os
import wouso.utils.user_util

# Setup Django environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wouso.settings")

from django.contrib.auth.models import User

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Usage: %s permission-string" % (sys.argv[0])
        sys.exit(1)

    count = 0
    for u in User.objects.all():
        if u.has_perm('files.can_list_files'):
            count += 1

    print count

if __name__ == "__main__":
    sys.exit(main())
