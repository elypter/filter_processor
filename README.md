# filter_processor
toolchain to create generic filterlists from other lists and keywords

# create_lists.sh
This shellscript executes the scripts below with different parameters to create a variety of lists

# rule_keyword_generator.py
A script that looks for names of classes and ids in cosmetic adblock/ublock rules for the use in heuristic filters
sticky_keyword_generator.py this script

# header_filter_creator.py
A generic filter for adblockers that keeps annoying sticky header and footer bars from filling up your screen.
prefixes.txt and suffixes.txt are lists of frequently used words that when combined make up names for classes or styles of annoying sticky elements like #header bars.

# decoy_generic_filter.py
This script takes a list of generic cosmetic filters as input and turns them into a pseudo generic list by creating a
specific rule for each of the most popular tlds for each rule. this makes the filterlist a lot larger but it is neccesary
to get around ublocks condescending limitation to disallow generic cosmetic filters.
using a generic cosmetic filter is bad practice if it can be avoided but sometimes this is not possible.

# legacy_generic_header_filter_creator.py
used to do what header_filter_creator.py and decoy_generic_filter.py did in one script.
