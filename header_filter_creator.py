#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#A generic filter for adblockers that keeps annoying sticky header and footer bars from filling up your screen.
#
#prefixes.txt and suffixes.txt are lists of frequently used words that when combined make up names for classes or styles of annoying sticky elements like #header bars.
#
#License: GPL-3.0

#todo:
#Capital Letters
#_ underscore
#singles.txt

from StringIO import StringIO
from collections import defaultdict
import operator
import argparse
import os
import sys

defaults=[]
for default_file in ["sources/prefixes.txt","sources/suffixes.txt","sources/dprefixes.txt","sources/header.txt"]:
    try:
        defaults.append(open(default_file))
    except:
        print("defaults file "+default_file+" cannot be read")
        defaults.append(os.devnull)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="A generic filter for adblockers that keeps annoying sticky header and footer bars from filling up your screen."
""
"prefixes.txt and suffixes.txt are lists of frequently used words that when combined make up names for classes or styles of annoying sticky elements like #header bars.")

parser.add_argument('-prefixes', nargs='*', type=argparse.FileType('r'), default=defaults[0], help="prefixes file which contains keywords that are often the first part of a class or style name of a sticky bar")
parser.add_argument('-suffixes', nargs='*', type=argparse.FileType('r'), default=defaults[1], help="suffixes file which contains keywords that are often the last part of a class or style name of a sticky bar")
parser.add_argument('-dprefixes', nargs='*', type=argparse.FileType('r'), default=defaults[2], help="file with prefixes that must only be used in combination with a suffix")
parser.add_argument('-header', nargs='?', type=argparse.FileType('r'), default=defaults[3], help="file that contains the header part of the filterlist")
parser.add_argument('-outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="file the generated list is written to")
args=parser.parse_args()

prefixes=[]
for prefix_file in args.prefixes:
    prefixes+=prefix_file.readlines()

suffixes=[]
for suffix_file in args.suffixes:
    suffixes+= suffix_file.readlines()

dprefixes=[]
for dprefix_file in args.dprefixes:
    dprefixes+= dprefix_file.readlines()

print("creating list")

#comments and general data of the filterlist
filters=[]
for headline in args.header.readlines():
    filters += [headline.strip()]

#all prefixes and suffixes and create combinations with a dash connecting prefix and suffix or without and for both styles and classes
for prefix in prefixes:
    prefix=prefix.strip()
    filters += ['##div[class*="' + prefix + '"]' + ":style(position: static!important)"]
    filters += ['##div[id*="' + prefix + '"]' + ":style(position: static!important)"]
for dprefix in dprefixes:
    dprefix = dprefix.strip()
    for suffix in suffixes:
        suffix=suffix.strip()
        if (not dprefix==suffix) & (dprefix!="") & (suffix!=""):
            filters += ["##div" + '[class*="' + dprefix + '"]' + '[class$="' + suffix + '"]' + ":style(position: static!important)"]
            filters += ["##div" + '[id*="' + dprefix + '"]' + '[id="' + suffix + '"]' + ":style(position: static!important)"]

#write list to disk
print("writing to disk")
outfile = open('domainless_header_list.txt', 'w')

for line in filters:
  args.outfile.write("%s\n" % line)
args.outfile.close()
