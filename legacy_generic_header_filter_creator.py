#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#A generic filter for adblockers that keeps annoying header and footer bars from filling up your screen.
#
#generic_header_list.txt is the actual filter list. it is 3.1Mb which is a lot for a filter list but i havent noticed any slowdown
#
#generic_header_filter.py is the script used to create the filterlist. due to limitations in ublock it is not possible to use this type of cosmetic filters #for all pages so the list has to have a rule for each top level domain. thats why this filter only works for the 20 most used top level domains. more can #be used by adjusting the value in the script
#
#prefixes.txt and suffixes.txt are lists of frequently used words that when combined make up names for classes or styles of annoying sticky elements like #header bars.
#
#License: GPL-3.0

#todo:
#Capital Letters
#_ underscore
#singles.txt

domain_number=20 #the top x top level domains to use. the more the more matches but also the bigger the file. 20 results in a 3Mb file


from StringIO import StringIO
from zipfile import ZipFile
from urllib2 import urlopen
from urlparse import urlparse
from collections import defaultdict
import operator

#old method of fetching tlds
#response = urlopen('https://web.archive.org/web/20111219160932id_/https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
#tlds = response.readlines()[1:]

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

#open prefixes file which contains keywords that are often the first part of a class or style name of a sticky bar
with open("sources/prefixes.txt") as f:
    prefixes = f.readlines()

#same as above, just the second part
with open("sources/suffixes.txt") as f:
    suffixes = f.readlines()

#prefixes that must only be used in combination with a suffix
with open("sources/dprefixes.txt") as f:
    dprefixes = f.readlines()
dprefixes = [dprefix.strip() for dprefix in dprefixes] #strip is used here because there is no loop to do it in like for prefixes and suffixes

print("creating list for")

#comments and general data of the filterlist
filters=[]
filters+=["[uBlock Origin 1.14.8+]"]
filters+=["! Title: generic annoying stickybar filter"]
filters+=["! Description: A generic list that makes annoying sticky headers unsticky"]
filters+=["! Expires: 14 days"]
filters+=["! Author: elypter"]
filters+=["! Homepage: https://github.com/elypter/generic_annoying_stickybar_filter"]
filters+=["! Support: https://github.com/elypter/generic_annoying_stickybar_filter/issues"]
filters+=["! Download: https://raw.githubusercontent.com/elypter/generic_annoying_stickybar_filter/master/prefixes.txt"]
filters+=["! License: GPL-3.0"]
filters+=["! "]

#loop over the first x tld domains, all prefixes and suffixes and create combinations with a dash connecting prefix and suffix or without and for bothstyles and classes
for i in range(domain_number):
    tld="*."+sorted_tlds[i][0]
    print("  "+tld)
    for prefix in prefixes:
        prefix=prefix.strip()        
        if not (prefix in dprefixes):                    
            filters+=[tld+"##."+prefix+":style(position: relative !important; top: 0 !important;)"]
            filters+=[tld+"###"+prefix+":style(position: relative !important; top: 0 !important;)"]        
        for suffix in suffixes:
            suffix=suffix.strip()
            if (not prefix==suffix) & (prefix!="") & (suffix!=""):
                filters+=[tld+"##."+prefix+suffix+":style(position: relative !important; top: 0 !important;)"]
                filters+=[tld+"##."+prefix+"-"+suffix+":style(position: relative !important; top: 0 !important;)"]
                filters+=[tld+"###"+prefix+suffix+":style(position: relative !important; top: 0 !important;)",]
                filters+=[tld+"###"+prefix+"-"+suffix+":style(position: relative !important; top: 0 !important;)"]

#if xpath and regex worked a lot of redundancy could be removed. maybe it does but i could not get this to work.
#for tld in tlds:
#    tld=tld.strip()
#    filters+=[tld+"##:xpath(.//*[matches(@class,'(sticky|header|head|navigation|nav|fixed|fix|ribbon|logo|app|footer|locked|main|top|pinned|banner|social|share|sharing|shares|like|follow|login|teaser|tease|related|recommend|recommended|action|scrolled|stuck|smart|mobile|index|icon|pagenav|row|static|tray|global|rail|tab|float|floating|scrolled|menu|bar|bottom|panel|mast|master)[_-]?(menu|bar|header|head|main|top|banner|sticky|navigation|nav)?')]:style(position:fixed))"]


#write list to disk
print("writing to disk")
outfile = open('generated_filterlists/generic_header_list.txt', 'w')

for line in filters:
  outfile.write("%s\n" % line)
outfile.close()
