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

def main():
    active_quizzes = Quiz.objects.filter(status='A')
    for q in active_quizzes:
        user_quizzes = UserToQuiz.objects.filter(quiz=q)
        for uq in user_quizzes:
            attempts = QuizAttempt.objects.filter(user_to_quiz=uq)
            if not attempts:
                continue
            a = attempts[0]
            user = uq.user
            try:
                player = Player.objects.get(user=user)
            except Exception, e:
                continue
            print '"%s","%s","%s","%d"' %(q.name, player.race.title, player.full_name, a.points)

if __name__ == "__main__":
    sys.exit(main())
