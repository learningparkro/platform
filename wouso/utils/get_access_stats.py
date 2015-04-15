#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/get_quiz_users.py

import codecs
import sys
import os

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# Setup Django environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wouso.settings")

from django.contrib.auth.models import User
from wouso.core.user.models import Race
from wouso.core.user.models import Player
from wouso.interface.activity.models import Activity

def main():
    access_activities = Activity.objects.filter(message_string='joined the game.')
    for a in access_activities:
        player = a.user_from
        print '"%s","%s","%s"' %(str(a.timestamp), player.race.title, player.full_name)

if __name__ == "__main__":
    sys.exit(main())
