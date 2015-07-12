#!/usr/bin/env python

import sys
import os
import csv

def main():
    if len(sys.argv) != 3:
        print >> sys.stderr, "%s input-file.csv to-replace-file.csv" %(sys.argv[0])
        sys.exit(1)

    input_file = open(sys.argv[1], "r")
    to_replace_file = open(sys.argv[2], "r")

    csv_input = csv.reader(input_file, delimiter=',')
    csv_replace = csv.reader(to_replace_file, delimiter=',')

    replace_array = []
    for row in csv_replace:
        replace_array.append({
            "username": row[0],
            "email": row[1]
            })

    for row in csv_input:
        username, first_name, last_name, email, password, school = row
        for e in replace_array:
            if e["email"] == email:
                username = e["username"]
        print "%s,%s,%s,%s,%s,%s" % (username, first_name, last_name, email, password, school)

if __name__ == "__main__":
    sys.exit(main())
