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
from wouso.core.user.models import Race
from wouso.core.user.models import Player

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Usage: %s permission-string" % (sys.argv[0])
        sys.exit(1)

    count = 0
    for p in Player.objects.all():
        if not p:
            print "Player account for username %s not found." %(u.username)
            continue
        if not p.race:  # Player with no race (such as admin).
            continue
        if p.race.can_play == False:
            continue

        u = p.user
        if not u.has_perm(sys.argv[1]):
            continue

        count += 1

    print count

if __name__ == "__main__":
    sys.exit(main())
