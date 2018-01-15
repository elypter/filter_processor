#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#A script that looks for names of classes and ids in cosmetic adblock/ublock rules for the use in heuristic filters
#sticky_keyword_generator.py this script
#generic_rule_names.txt whole classes and ids
#generic_rule_prefixes.txt the first up to n-1th part of a name seperated by "-"
#generic_rule_suffixes.txt the last part of a name seperated by "-"
#generic_rule_singles.txt names that cannot be seperated by "-"
#generic_rule_keywords.txt prefixes, suffixes and singles combined
#ignore_keywords.txt keywords that will be excluded from keywords.txt

#License: GPL3.0

from StringIO import StringIO
from urllib2 import urlopen
from urlparse import urlparse
from collections import defaultdict
import re
import operator
import os
import argparse

default_ignore_list = os.devnull
try:
    default_ignore_list = open("sources/ignore_keywords.txt")
except:
    print("defaults file " + "sources/ignore_keywords.txt" + " cannot be read")


parser = argparse.ArgumentParser(description="A script that looks for names of classes and ids in cosmetic adblock/ublock rules for the use in heuristic filters"
"sticky_keyword_generator.py this script")

parser.add_argument('source', type=str, help="the URL of a filterlist that should be downloaded and processed")
parser.add_argument('-min_keyword', type=int, default=3, help="words shorter than this number will not be included in any list. 0 means any word passes (default:3)")
parser.add_argument('-min_keyword_score', type=int, default=5, help="everytime a word is detected in the source the score for this words is increases by 1 words shorter than this number will not be included in any list. 0 means every score passes.(default:5)")
parser.add_argument('-max_list_len', type=int, default=0, help="the maximum lenth of each list. generic_rule_keywords.txt can be 3 times as long. 0 means no limit (default:0)")
parser.add_argument('-ignore_list', type=argparse.FileType('r'), default=default_ignore_list, nargs='*', help="the keywords contained in this list will be ignored")
parser.add_argument('-output_prefix', type=str, default="generic_rule_", help="this string will be added in front of the output path of each written file")
args=parser.parse_args()


#source='https://raw.githubusercontent.com/yourduskquibbles/webannoyances/master/ultralist.txt'

#fetching rules from.
print("downloading rules from " + args.source + "...")
response = urlopen(args.source)
print("processing...")
lines = response.readlines()

#these dicts contain the list for the respective files key:word value:score
l_names = defaultdict()
l_prefixes = defaultdict()
l_suffixes = defaultdict()
l_singles = defaultdict()
l_keywords = defaultdict()

#load the list of ignored keywords
ignore_keywords=[]
for ignore_keywords_list in args.ignore_list:
    ignore_keywords+=ignore_keywords_list.readlines()
ignore_keywords = [ignore_keyword.strip() for ignore_keyword in ignore_keywords]

for line in lines: #for each rule in the source
    element = re.search(r'(?:###|##\.)([0-9a-zA-Z\._-]+)', line)#extract the id/class names
    if element:
        names = element.group(1).split(".")#split multiple classes separated by dots
        for name in names:#for each of those classes or the id
            if len(name)>=args.min_keyword and not name in ignore_keywords: #check if above minimum length and if not excluded
                if (not name in l_names):#check if key already exists. increments if it does, initializes with 1 if not
                    #l_names+=[name]
                    l_names[name]=1
                else:
                    l_names[name] += 1
            subnames=name.split("-")#further split by -
            if len(subnames)>1:
                for i in range(len(subnames)):
                    if len(subnames[0]) >= args.min_keyword and not subnames[0] in ignore_keywords:
                        if not subnames[0] in l_keywords:
                            #l_keywords += [subnames[0]]
                            l_keywords[subnames[0]]=1
                        else:
                            l_keywords[subnames[0]] += 1
                    if i==len(subnames)-1:#suffixes are only the last part of a split classname/id
                        if len(subnames[0]) >= args.min_keyword and not subnames[0] in ignore_keywords:
                            if not subnames[i] in l_suffixes:
                                #l_suffixes+=[subnames[i]]
                                l_suffixes[subnames[i]]=1
                            else:
                                l_suffixes[subnames[i]] += 1
                    else:
                        if len(subnames[i]) >= args.min_keyword and not subnames[i] in ignore_keywords:
                            if not subnames[i] in l_prefixes:
                                #l_prefixes+=[subnames[i]]
                                l_prefixes[subnames[i]]=1
                            else:
                                l_prefixes[subnames[i]] += 1
            else:
                if (len(subnames[0]) >= args.min_keyword) and (not subnames[0] in ignore_keywords):
                    if not subnames[0] in l_keywords:
                        #l_keywords += [subnames[0]]
                        l_keywords[subnames[0]]=1
                    else:
                        l_keywords[subnames[0]] += 1
                    if not subnames[0] in l_singles:
                        #l_singles += [subnames[0]]
                        l_singles[subnames[0]]=1
                    else:
                        l_singles[subnames[0]] += 1

#sort all dicts by descending score
l_names = sorted(l_names.items(), key=operator.itemgetter(1), reverse=True)
l_prefixes = sorted(l_prefixes.items(), key=operator.itemgetter(1), reverse=True)
l_suffixes = sorted(l_suffixes.items(), key=operator.itemgetter(1), reverse=True)
l_singles = sorted(l_singles.items(), key=operator.itemgetter(1), reverse=True)
l_keywords = sorted(l_keywords.items(), key=operator.itemgetter(1), reverse=True)


#write list to disk
print("writing to disk")

#writing each dict to corresponding file and terminate at max_list_len(if it is not 0) or if the score is below threshold
outfile = open(args.output_prefix+'names.txt', 'w')
i=0
for line in l_names:
  if (line[1]<args.min_keyword_score and args.min_keyword_score>0) or (i>=args.max_list_len and args.max_list_len>0):
      print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
      break
  outfile.write("%s\n" % line[0])
  i+=1
outfile.close()

outfile = open(args.output_prefix+'prefixes.txt', 'w')
i=0
for line in l_prefixes:
    if (line[1] < args.min_keyword_score and args.min_keyword_score > 0) or (i >= args.max_list_len and args.max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()

outfile = open(args.output_prefix+'suffixes.txt', 'w')
i=0
for line in l_suffixes:
    if (line[1] < args.min_keyword_score and args.min_keyword_score > 0) or (i >= args.max_list_len and args.max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()

outfile = open(args.output_prefix+'singles.txt', 'w')
i=0
for line in l_singles:
    if (line[1] < args.min_keyword_score and args.min_keyword_score > 0) or (i >= args.max_list_len and args.max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()

outfile = open(args.output_prefix+'keywords.txt', 'w')
i=0
for line in l_keywords:
    if (line[1] < args.min_keyword_score and args.min_keyword_score > 0) or (i >= args.max_list_len*3 and args.max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()