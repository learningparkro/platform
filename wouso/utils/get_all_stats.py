#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/get_stats.py

import sys
import csv
import os
import wouso.utils.user_util
import codecs

# Setup Django environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wouso.settings")

from django.contrib.auth.models import User
from wouso.core.user.models import Race
from wouso.core.user.models import Player
from wouso.interface.apps.lesson.models import Lesson, LessonTag, LessonCategory
from wouso.games.quiz.models import Quiz, QuizCategory, QuizUser, UserToQuiz, QuizAttempt
from wouso.core.qpool.models import Question, Answer, Tag, Category

from django.db.models import Q


def main():
    # Get number of lessons.
    for lc in LessonCategory.objects.all():
        num_lessons = 0
        for lt in LessonTag.objects.filter(category=lc):
            num_lessons += len(Lesson.objects.filter(tag=lt))
        print "%s: %d" % (lc.name, num_lessons)

    # Get number of quizzes (public and internal).
    for qc in QuizCategory.objects.all():
        expired_quizzes = len(Quiz.objects.filter(category=qc, status='E'))
        active_quizzes = len(Quiz.objects.filter(category=qc, status='A'))
        inactive_quizzes = len(Quiz.objects.filter(category=qc, status='I'))
        print "%s, active: %u, inactive: %u, expired: %u" % (qc.name, active_quizzes, inactive_quizzes, expired_quizzes)

    # Get number of questions.
    qstats = [
            {
                "category": "Chimie",
                "tags": [ "Tomas I", "Tomas II", "Tomas III", "Tomas IV", "Echilibru chimic", "Electrochimie", "Termochimie", "Cinetica chimica", "Chimie anorganica", "Echilibru chimic (final)", "Cinetica chimica (final)", "Termochimie (final)", "Electrochimie (final)", "Chimie organica I (final)", "Chimie organica II (final)", "Chimie organica III (final)", "Chimie organica IV (final)" ],
                "num_questions": 0,
                },
            {
                "category": u"Fizică",
                "tags": [ "Mecanica", "Termodinamica", "Curent continuu", "Optica", "Mecanica (final)", "Termodinamica (final)", "Electricitate (final)" , "Optica (final)" ],
                "num_questions": 0,
                },
            {
                "category": u"Matematică",
                "tags": [ "Matematica I", "Matematica II", "Matematica III", "Matematica (final)" ],
                "num_questions": 0,
                }
            ]
    for entry in qstats:
        for tname in entry["tags"]:
            t = Tag.objects.get(name=tname)
            entry["num_questions"] += len(Question.objects.filter(tags=t))
        print "%s: %u" % (entry["category"], entry["num_questions"])

    # Get number of student accounts.
    num_student_accounts = len(Player.objects.filter(race__can_play=True))
    print "student accounts: %u" % (num_student_accounts)
    num_student_logged_in_accounts = len(Player.objects.filter(race__can_play=True).exclude(last_seen__isnull=True))
    print "student logged in accounts: %u" % (num_student_logged_in_accounts)

    # Get number of team and teacher accounts.
    num_team_accounts = len(Player.objects.filter(Q(race__name='csapcs') | Q(race__name='profesori') | Q(race__name='coordonatori')))
    print "team accounts: %u" % (num_team_accounts)
    num_team_logged_in_accounts = len(Player.objects.filter(Q(race__name='csapcs') | Q(race__name='profesori') | Q(race__name='coordonatori')).exclude(last_seen__isnull=True))
    print "team logged in accounts: %u" % (num_team_logged_in_accounts)

    # Get number of other accounts.
    num_other_accounts = len(Player.objects.all()) - num_student_accounts - num_team_accounts
    print "other accounts: %u" % (num_other_accounts)
    num_other_logged_in_accounts = len(Player.objects.exclude(last_seen__isnull=True)) - num_student_logged_in_accounts - num_team_logged_in_accounts
    print "other logged in accounts: %u" % (num_other_logged_in_accounts)

    for qc in QuizCategory.objects.all():

        # Get number of student test accesses.
        num_student_quiz_attempts = len(QuizAttempt.objects.filter(user_to_quiz__user__race__can_play=True, user_to_quiz__quiz__category=qc, date__lte="2015-06-30"))
        print "student quiz attempts: %s: %u" % (qc, num_student_quiz_attempts)
        num_student_quiz_accesses = len(UserToQuiz.objects.filter(user__race__can_play=True, quiz__category=qc, start__lte="2015-06-30"))
        print "student quiz accesses: %s: %u" % (qc, num_student_quiz_accesses)

        # Get number of team and teacher test accesses.
        num_team_quiz_attempts = len(QuizAttempt.objects.filter(Q(user_to_quiz__user__race__name='csapcs') | Q(user_to_quiz__user__race__name='profesori') | Q(user_to_quiz__user__race__name='coordonatori'), user_to_quiz__quiz__category=qc, date__lte="2015-06-30"))
        print "team quiz attempts: %s: %u" % (qc, num_team_quiz_attempts)
        num_team_quiz_accesses = len(UserToQuiz.objects.filter(Q(user__race__name='csapcs') | Q(user__race__name='profesori') | Q(user__race__name='coordonatori'), quiz__category=qc, start__lte="2015-06-30"))
        print "team quiz accesses: %s: %u" % (qc, num_team_quiz_accesses)

        # Get number of other test accesses.
        num_other_quiz_attempts = len(QuizAttempt.objects.filter(user_to_quiz__quiz__category=qc, date__lte="2015-06-30")) - num_student_quiz_attempts - num_team_quiz_attempts
        print "other quiz attempts: %s: %u" % (qc, num_other_quiz_attempts)
        num_other_quiz_accesses = len(UserToQuiz.objects.filter(quiz__category=qc, start__lte="2015-06-30")) - num_student_quiz_accesses - num_team_quiz_accesses
        print "other quiz accesses: %s: %u" % (qc, num_other_quiz_accesses)


if __name__ == "__main__":
    sys.exit(main())
