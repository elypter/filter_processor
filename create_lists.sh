#!/bin/sh

echo "extraction_based:"
echo "loading ultralist and extracting keywords:"
./rule_keyword_generator.py https://raw.githubusercontent.com/yourduskquibbles/webannoyances/master/ultralist.txt -ignore_list sources/ignore_keywords.txt  -output_prefix rules/generic_rule_ -min_keyword 3 -min_keyword_score 8
echo "creating generic extraction based filter file:"
./header_filter_creator.py -prefixes rules/generic_rule_prefixes.txt -suffixes rules/generic_rule_suffixes.txt -dprefixes sources/dprefixes.txt -header sources/decoy_generic_extraction_blockhead_header.txt -outfile temp/generic_extraction_blockhead.txt
echo "creating decoy generic extraction based filter file:"
./decoy_generic_filter.py -tlds 20 -infile temp/generic_extraction_blockhead.txt -outfile "generated_filterlists/blockhead(decoy_generic_extraction).txt"
./decoy_generic_filter.py -tlds 100 -infile temp/generic_extraction_blockhead.txt -outfile "generated_filterlists/blockhead(decoy_generic_extraction_xdomains).txt"

echo "loading ultralist and extracting keywords:"
./rule_keyword_generator.py https://raw.githubusercontent.com/yourduskquibbles/webannoyances/master/ultralist.txt -ignore_list sources/ignore_keywords.txt  -output_prefix rules/generic_rule_plus_ -min_keyword 3 -min_keyword_score 2
echo "creating generic extraction based filter file:"
./header_filter_creator.py -prefixes rules/generic_rule_plus_prefixes.txt -suffixes rules/generic_rule_plus_suffixes.txt -dprefixes sources/dprefixes.txt -header sources/decoy_generic_extraction_blockhead_header.txt -outfile rules/generic_extraction_plus_blockhead.txt
echo "creating decoy generic extraction based filter file:"
./decoy_generic_filter.py -tlds 20 -infile temp/generic_extraction_plus_blockhead.txt -outfile "generated_filterlists/blockhead(decoy_generic_extraction_plus).txt"
./decoy_generic_filter.py -tlds 100 -infile temp/generic_extraction_plus_blockhead.txt -outfile "generated_filterlists/blockhead(decoy_generic_extraction_xdomains_plus).txt"

echo "selection_based:"
echo "creating generic selection based filter file:"
./header_filter_creator.py -prefixes sources/prefixes.txt -suffixes sources/suffixes.txt -dprefixes sources/dprefixes.txt -header sources/decoy_generic_selection_blockhead_header.txt -outfile temp/generic_selection_blockhead.txt
echo "creating decoy generic selection based filter file:"
./decoy_generic_filter.py -tlds 20 -infile temp/generic_selection_blockhead.txt -outfile "generated_filterlists/blockhead(decoy_generic_selection).txt"
./decoy_generic_filter.py -tlds 100 -infile temp/generic_selection_blockhead.txt -outfile "generated_filterlists/blockhead(decoy_generic_selection_xdomains).txt"
