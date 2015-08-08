#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/get_quiz_users.py

import codecs
import sys
import os
from datetime import datetime

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
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: %s start_date end_date" % (sys.argv[0])
        print >> sys.stderr, "\tdata format: YYYY-MM-DD"
        sys.exit(1)

    start_date = None
    end_date = None
    try:
        start_date = datetime.strptime(sys.argv[1], "%Y-%m-%d")
    except Exception, e:
        print >> sys.stderr, "Error: start date must be in YYYY-MM-DD format"
        print e
        sys.exit(1)
    try:
        end_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    except Exception, e:
        print >> sys.stderr, "Error: end date must be in YYYY-MM-DD format"
        sys.exit(1)

    if start_date > end_date:
        print >> sys.stderr, "Error: start date is after end date"
        sys.exit(1)

    quiz_range_stats = []
    active_quizzes = Quiz.objects.filter(Q(status='A') | Q(status='E'))
    for q in active_quizzes:
        quiz_stat = {
                "quiz": q.name,
                "attempts": 0,
                "students": 0,
                "average": float(0),
                "maximum": q.points_reward
                }

        total_points = 0
        user_quizzes = UserToQuiz.objects.filter(quiz=q)
        for uq in user_quizzes:
            attempts = QuizAttempt.objects.filter(user_to_quiz=uq, date__range=[start_date, end_date])
            if not attempts:
                continue
            a = attempts[0]
            total_points += a.points
            quiz_stat["attempts"] += len(attempts)
            quiz_stat["students"] += 1

        if quiz_stat["attempts"] == 0:
            quiz_stat["average"] = float(0)
        else:
            quiz_stat["average"] = float(total_points) / quiz_stat["attempts"]

        quiz_range_stats.append(quiz_stat)

    print "quiz,students,attempts,average,maximum"
    for s in quiz_range_stats:
        print "%s,%u,%u,%.2f,%u" % (s["quiz"], s["students"], s["attempts"], s["average"], s["maximum"])


if __name__ == "__main__":
    sys.exit(main())
