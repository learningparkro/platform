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
from wouso.games.quiz.models import Quiz, QuizUser, UserToQuiz, QuizAttempt
from wouso.interface.activity.models import Activity
from django.db.models import Q

def main():
    data = {}
    for r in Race.objects.all():
        num_players = len(Player.objects.filter(race=r))
        data[r] = {
                'accounts': num_players,
                'accessed_accounts': 0,
                'num_logins': 0,
                'anorg_chem_test': 0,
                'org_chem_test': 0,
                'electricity_test': 0,
                'mechanics_test': 0,
                'optics_test': 0,
                'thermodynamics_test': 0,
                'math_test': 0,
                'anorg_chem_test_final': 0,
                'org_chem_test_final': 0,
                'electricity_test_final': 0,
                'mechanics_test_final': 0,
                'optics_test_final': 0,
                'thermodynamics_test_final': 0,
                'math_test_final': 0
                }

    active_quizzes = Quiz.objects.filter(Q(status='A') | Q(status='E'))
    for q in active_quizzes:
        user_quizzes = UserToQuiz.objects.filter(quiz=q)
        for uq in user_quizzes:
            attempts = QuizAttempt.objects.filter(user_to_quiz=uq)
            if not attempts:
                continue
            try:
                player = Player.objects.get(id=uq.user.id)
            except Exception, e:
                continue
            if q.id == 22:
                data[player.race]['anorg_chem_test'] += 1
            if q.id == 21:
                data[player.race]['org_chem_test'] += 1
            if q.id == 41:
                data[player.race]['electricity_test'] += 1
            if q.id == 39:
                data[player.race]['mechanics_test'] += 1
            if q.id == 42:
                data[player.race]['optics_test'] += 1
            if q.id == 40:
                data[player.race]['thermodynamics_test'] += 1
            if q.id == 43:
                data[player.race]['math_test'] += 1
            if q.id == 70:
                data[player.race]['anorg_chem_test_final'] += 1
            if q.id == 69:
                data[player.race]['org_chem_test_final'] += 1
            if q.id == 67:
                data[player.race]['electricity_test_final'] += 1
            if q.id == 65:
                data[player.race]['mechanics_test_final'] += 1
            if q.id == 68:
                data[player.race]['optics_test_final'] += 1
            if q.id == 66:
                data[player.race]['thermodynamics_test_final'] += 1
            if q.id == 52:
                data[player.race]['math_test_final'] += 1

    access_activities = Activity.objects.filter(message_string='joined the game.')
    for a in access_activities:
        player = a.user_from
        data[player.race]['accessed_accounts'] += 1

    login_activities = Activity.objects.filter(action='login')
    for a in login_activities:
        player = a.user_from
        data[player.race]['num_logins'] += 1

    print u"Grup,Conturi existente,Conturi accesate,Procentaj de accesare,Număr de autentificări,Chimie anorganică,Chimie anorganică (final),Chimie organică,Chimie organică (final),Electricitate,Electricitate (final),Mecanică,Mecanică (final),Optică,Optică (final),Termodinamică,Termodinamică (final),Matematică,Matematică (final)"
    for key, value in data.iteritems():
        print "%s,%d,%d,%.2f,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" %(key.title,
                value['accounts'], value['accessed_accounts'],
                float(value['accessed_accounts']) / value['accounts'],
                value['num_logins'],
                value['anorg_chem_test'], value['anorg_chem_test_final'],
                value['org_chem_test'], value['org_chem_test_final'],
                value['electricity_test'], value['electricity_test_final'],
                value['mechanics_test'], value['mechanics_test_final'],
                value['optics_test'], value['optics_test_final'],
                value['thermodynamics_test'], value['thermodynamics_test_final'],
                value['math_test'], value['math_test_final'])

if __name__ == "__main__":
    sys.exit(main())
