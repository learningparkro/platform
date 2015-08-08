#!/usr/bin/env python

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/get_quiz_for_user_list.py <user-list-file> <quiz-name>

import sys
import os
import codecs


reload(sys)
sys.setdefaultencoding('utf8')

# Setup Django environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wouso.settings")

from django.contrib.auth.models import User
from wouso.core.user.models import Player
from wouso.games.quiz.models import Quiz, QuizUser, UserToQuiz, QuizAttempt


UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


def print_by_type(p, q, type):
    qal = QuizAttempt.objects.filter(user_to_quiz__quiz=q, user_to_quiz__user=p)
    if not qal:
        return
    qal_sorted = QuizAttempt.objects.filter(user_to_quiz__quiz=q, user_to_quiz__user=p).order_by('points')
    date = qal[0].date.strftime("%Y-%m-%d %H:%M")

    if type == "noresult":
        print '"%s","%s","%s","%s","%s"' % (p.nickname, p.user.first_name, p.user.last_name, p.race.name, p.race.title)
    elif type == "first":
        points = qal[0].points
        grade = float(points) / q.points_reward * 10
        print '"%s","%s","%s","%s","%s","%s","%d","%.2f"' % (p.nickname, p.user.first_name, p.user.last_name, p.race.name, p.race.title, date, points, grade)
    elif type == "last":
        points = qal[len(qal)-1].points
        grade = float(points) / q.points_reward * 10
        print '"%s","%s","%s","%s","%s","%s","%d","%.2f"' % (p.nickname, p.user.first_name, p.user.last_name, p.race.name, p.race.title, date, points, grade)
    elif type == "first_non_zero":
        points = 0
        for qa in qal:
            if qa.points > 0:
                points = qa.points
                break
        grade = float(points) / q.points_reward * 10
        print '"%s","%s","%s","%s","%s","%s","%d","%.2f"' % (p.nickname, p.user.first_name, p.user.last_name, p.race.name, p.race.title, date, points, grade)
    elif type == "best":
        points = qal_sorted[len(qal_sorted)-1].points
        grade = float(points) / q.points_reward * 10
        print '"%s","%s","%s","%s","%s","%s","%d","%.2f"' % (p.nickname, p.user.first_name, p.user.last_name, p.race.name, p.race.title, date, points, grade)
    elif type == "worst":
        points = qal_sorted[0].points
        grade = float(points) / q.points_reward * 10
        print '"%s","%s","%s","%s","%s","%s","%d","%.2f"' % (p.nickname, p.user.first_name, p.user.last_name, p.race.name, p.race.title, date, points, grade)
    elif type == "worst_non_zero":
        points = 0
        for qa in qal_sorted:
            if qa.points > 0:
                points = qa.points
                break
        grade = float(points) / q.points_reward * 10
        print '"%s","%s","%s","%s","%s","%s","%d","%.2f"' % (p.nickname, p.user.first_name, p.user.last_name, p.race.name, p.race.title, date, points, grade)


def main():
    if len(sys.argv) != 4:
        print >> sys.stderr, "%s <user-list-file> <quiz-name> <type>" % (sys.argv[0])
        sys.exit(1)

    try:
        q = Quiz.objects.get(name=sys.argv[2])
    except Exception, e:
        print >> sys.stderr, "No such quiz %s" % (sys.argv[2])
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        for line in f:
            nickname = line.strip()
            try:
                p = Player.objects.get(nickname=nickname)
            except Exception, e:
                print >> sys.stderr, "No such player %s" % (nickname)
                continue
            print_by_type(p, q, sys.argv[3])


if __name__ == "__main__":
    sys.exit(main())
