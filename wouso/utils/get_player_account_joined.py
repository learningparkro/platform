#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/get_player_account_joined.py

import codecs
import sys
import os
import datetime

utf8writer = codecs.getwriter('utf8')
sys.stdout = utf8writer(sys.stdout)

# Setup Django environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wouso.settings")

from django.contrib.auth.models import User
from wouso.core.user.models import Race
from wouso.core.user.models import Player
from wouso.interface.activity.models import Activity

def main():
    players = Player.objects.all()

    for p in players:
        if p.race == None:
            continue
        u = p.user
        #if u.date_joined < datetime.datetime(2015,1,11,0,0,0) and u.date_joined >= datetime.datetime(2015,1,10,0,0,0):
        print '"%s","%s","%s"' %(str(u.date_joined), p.race.title, p.full_name)

if __name__ == "__main__":
    sys.exit(main())
