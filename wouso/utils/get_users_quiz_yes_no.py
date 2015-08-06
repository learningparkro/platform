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
from django.db.models import Q
from wouso.core.user.models import Race
from wouso.core.user.models import Player
from wouso.games.quiz.models import Quiz, QuizUser, UserToQuiz, QuizAttempt

def main():
    initial_quiz = Quiz.objects.get(name='NOU: Evaluare inițială matematică (1h și 30 de minute, 150 de puncte)')
    initial_user_quizzes = UserToQuiz.objects.filter(quiz=initial_quiz)
    initial_quiz_users = []
    for uq in initial_user_quizzes:
        attempts = QuizAttempt.objects.filter(user_to_quiz=uq)
        if not attempts:
            continue
        initial_quiz_users.append(uq.user)

    final_quiz = Quiz.objects.get(name='Evaluare finală matematică (1h și 30 de minute, 150 de puncte)')
    final_user_quizzes = UserToQuiz.objects.filter(quiz=final_quiz)
    final_quiz_users = []
    for uq in final_user_quizzes:
        attempts = QuizAttempt.objects.filter(user_to_quiz=uq)
        if not attempts:
            continue
        final_quiz_users.append(uq.user)

    users_to_send_email_to = []
    for u in initial_quiz_users:
        if u not in final_quiz_users:
            users_to_send_email_to.append(u)

    for u in users_to_send_email_to:
        user = u.user
        print "%s,%s,%s,%s,%s,%s,%s" %(user.username, user.first_name, \
                user.last_name, user.email, user.is_active, user.is_staff, \
                user.is_superuser)

if __name__ == "__main__":
    sys.exit(main())
