#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#This script takes a list of generic cosmetic filters as input and turns them into a pseudo generic list by creating a
#specific rule for each of the most popular tlds for each rule. this makes the filterlist a lot larger but it is neccesary
#to get around ublocks condescending limitation to disallow generic cosmetic filters.
#using a generic cosmetic filter is bad practice if it can be avoided but sometimes this is not possible.
#
#for these situation, instead of banning reality i created this tool as a workaround
#
#License: GPL-3.0

from StringIO import StringIO
from zipfile import ZipFile
from urllib2 import urlopen
from urlparse import urlparse
from collections import defaultdict
import sys
import operator
import argparse
import os

parser = argparse.ArgumentParser(description="This script takes a list of generic cosmetic filters as input and turns them into a pseudo generic list by creating a"
"specific rule for each of the most popular tlds for each rule. this makes the filterlist a lot larger but it is neccesary"
"to get around ublocks condescending limitation to disallow generic cosmetic filters."
"using a generic cosmetic filter is bad practice if it can be avoided but sometimes this is not possible.")

parser.add_argument('-tlds', type=int, default=20, metavar="N", help="Use the first <N> top level domains (default:20)")
parser.add_argument('-infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file (default:<stdin>)")
parser.add_argument('-outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file (default:<stdout>)")
parser.add_argument('-headfile', nargs='?', type=argparse.FileType('r'), default=os.devnull, help="file that contains the header part of the filterlist (default:/dev/null)")
args=parser.parse_args()


#fetching alexas top 1 million most popular websites, counting occurences of top level domains and then sorting it by tld count.
print("downloading alexa top 1m(9,6Mb)...")
response = urlopen('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
archive = ZipFile(StringIO(response.read()))
print("loading...")
top1m = archive.open('top-1m.csv')
domains = top1m.readlines()
rankings = defaultdict(int)
for domain in domains:
    tld = domain.strip().split('.')[-1]
    rankings[tld]+=1
sorted_tlds = sorted(rankings.items(), key=operator.itemgetter(1), reverse=True)

filters=[]
for headlines in args.headfile.readlines():
    filters += [headline]

filterlines=args.infile.readlines()

#loop over the first x tld domains, all prefixes and suffixes and create combinations with a dash connecting prefix and suffix or without and for bothstyles and classes
for i in range(args.tlds):
    tld="*."+sorted_tlds[i][0]
    print("  "+tld)
    for filterline in filterlines:
        if filterline[0]=="#":
            filters += [tld+filterline]
        else:
            filters += [filterline]

#write list to disk
print("writing to disk")

for line in filters:
  args.outfile.write("%s" % line)
args.outfile.close()
