#!/usr/bin/env python

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/update_emails.py <path-to-csv-file>

import sys
import csv
import wouso.utils.user_util

def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s <file.csv>" % (sys.argv[0])
        print >> sys.stderr, " CSV columns: username, first name, last name, email, password, school_name"
        sys.exit(1)

    csvfile = open(sys.argv[1], 'r')
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        username = row[0]
        email = row[3]
        print "change username %s to email %s" % (username, email)
        try:
            ret = wouso.utils.user_util.update_user(username, email=email)
        except:
            print "Failed changing password for user %s." %(username)
            continue
        if ret:
            print "Successfully changed password for user %s." %(username)
        else:
            print "Failed changing password for user %s." %(username)


if __name__ == "__main__":
    sys.exit(main())
