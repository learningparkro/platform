#!/usr/bin/env python

# To test, run from parent folder using a command such as:
# PYTHONPATH=../:. python utils/update_usernames_by_emails.py <path-to-csv-file>

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
        first_name = row[1]
        email = row[3]
        try:
            ret = wouso.utils.user_util.update_user_by_email(email, first_name=first_name)
        except:
            print "Failed changing first name for email %s." %(email)
            continue
        if ret:
            print "Successfully changed first name for email %s." %(email)
        else:
            print "Failed changing first name for email %s." %(email)


if __name__ == "__main__":
    sys.exit(main())
